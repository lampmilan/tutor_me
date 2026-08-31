"""M6 production tests: CORS lock, rate limits, workspace TTL cleanup."""

from __future__ import annotations

import tempfile
import time
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import patch

from fastapi import Depends, FastAPI, Request
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import Session, sessionmaker

from app.config import Settings
from app.database import Base
from app.models import Exam, File, Submission, Workspace
from app.api.ops_auth import require_ops_token
from app.services.rate_limit import RATE_LIMIT_DETAIL, SlidingWindowLimiter, limit_execute, limiter
from app.services.workspace import cleanup_expired_workspaces, delete_workspace, touch_workspace


def _session() -> Session:
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()


class CorsSettingsTests(unittest.TestCase):
    def test_default_cors_field_is_not_wildcard(self) -> None:
        default = Settings.model_fields["cors_origins"].default
        self.assertIsInstance(default, str)
        self.assertNotEqual(default, "*")
        self.assertIn("localhost", default)

    def test_default_origins_are_localhost_not_wildcard(self) -> None:
        settings = Settings(cors_origins="http://localhost:3000,http://127.0.0.1:3000")
        origins = settings.cors_origin_list()
        self.assertNotIn("*", origins)
        self.assertIn("http://localhost:3000", origins)

    def test_production_origin_disables_vercel_regex(self) -> None:
        settings = Settings(
            cors_origins="https://erettsegi-lab.vercel.app",
            cors_origin_regex="",
        )
        kwargs = settings.cors_middleware_kwargs()
        self.assertEqual(kwargs["allow_origins"], ["https://erettsegi-lab.vercel.app"])
        self.assertIsNone(kwargs["allow_origin_regex"])
        self.assertFalse(kwargs["allow_credentials"])

    def test_optional_preview_regex(self) -> None:
        settings = Settings(
            cors_origins="https://erettsegi-lab.vercel.app",
            cors_origin_regex=r"https://.*\.vercel\.app",
        )
        kwargs = settings.cors_middleware_kwargs()
        self.assertEqual(kwargs["allow_origin_regex"], r"https://.*\.vercel\.app")

    def test_star_still_parses_for_local_escape_hatch(self) -> None:
        settings = Settings(cors_origins="*")
        self.assertEqual(settings.cors_origin_list(), ["*"])


class RateLimiterTests(unittest.TestCase):
    def test_allows_under_limit_then_blocks(self) -> None:
        limiter = SlidingWindowLimiter()
        self.assertTrue(limiter.allow("execute:1.1.1.1", 2, 60)[0])
        self.assertTrue(limiter.allow("execute:1.1.1.1", 2, 60)[0])
        allowed, retry = limiter.allow("execute:1.1.1.1", 2, 60)
        self.assertFalse(allowed)
        self.assertGreaterEqual(retry, 1)

    def test_separate_keys_are_independent(self) -> None:
        limiter = SlidingWindowLimiter()
        limiter.allow("execute:a", 1, 60)
        allowed, _ = limiter.allow("execute:b", 1, 60)
        self.assertTrue(allowed)

    def test_window_expiry_allows_again(self) -> None:
        limiter = SlidingWindowLimiter()
        self.assertTrue(limiter.allow("judge:ip", 1, 0.05)[0])
        self.assertFalse(limiter.allow("judge:ip", 1, 0.05)[0])
        time.sleep(0.06)
        self.assertTrue(limiter.allow("judge:ip", 1, 0.05)[0])

    def test_zero_max_disables_limit(self) -> None:
        limiter = SlidingWindowLimiter()
        for _ in range(5):
            self.assertTrue(limiter.allow("execute:x", 0, 60)[0])

    def test_hungarian_429_copy(self) -> None:
        self.assertIn("Túl sok kérés", RATE_LIMIT_DETAIL)


class RateLimitHttpTests(unittest.TestCase):
    def setUp(self) -> None:
        limiter.reset()
        app = FastAPI()

        @app.post("/execute")
        def execute(_: None = Depends(limit_execute)):
            return {"ok": True}

        self.client = TestClient(app)

    def tearDown(self) -> None:
        limiter.reset()

    def test_429_has_hungarian_detail_and_retry_after(self) -> None:
        settings = Settings(rate_limit_execute_per_minute=1, rate_limit_window_seconds=60)
        with patch("app.services.rate_limit.get_settings", return_value=settings):
            first = self.client.post("/execute")
            self.assertEqual(first.status_code, 200)
            second = self.client.post("/execute")
        self.assertEqual(second.status_code, 429)
        self.assertEqual(second.json()["detail"], RATE_LIMIT_DETAIL)
        self.assertIn("retry-after", {k.lower() for k in second.headers})


class WorkspaceTtlTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmpdir.cleanup)
        self.db = _session()
        self.exam = Exam(title="Demo", description="")
        self.db.add(self.exam)
        self.db.commit()
        self.db.refresh(self.exam)

    def _workspace(self, last_accessed: datetime, disk: bool = True) -> Workspace:
        ws = Workspace(
            exam_id=self.exam.id,
            user_id="anonymous",
            path="",
            created_at=last_accessed,
            last_accessed_at=last_accessed,
        )
        self.db.add(ws)
        self.db.flush()
        root = Path(self._tmpdir.name) / str(ws.id)
        if disk:
            root.mkdir(parents=True, exist_ok=True)
            (root / "main.py").write_text("print(1)\n", encoding="utf-8")
            ws.path = str(root)
        else:
            ws.path = str(root)
        self.db.add(
            File(workspace_id=ws.id, filename="main.py", content="print(1)\n", read_only=False)
        )
        self.db.add(Submission(workspace_id=ws.id, points_earned=0, points_possible=1))
        self.db.commit()
        self.db.refresh(ws)
        return ws

    def test_cleanup_deletes_idle_workspace_and_disk(self) -> None:
        old = self._workspace(_utcnow() - timedelta(days=10))
        fresh = self._workspace(_utcnow())
        old_path = Path(old.path)
        self.assertTrue(old_path.exists())

        with patch("app.services.workspace.get_settings") as mock_settings:
            mock_settings.return_value = Settings(workspace_ttl_days=7)
            deleted = cleanup_expired_workspaces(self.db)

        self.assertEqual(deleted, 1)
        self.assertIsNone(self.db.query(Workspace).filter(Workspace.id == old.id).first())
        self.assertIsNotNone(self.db.query(Workspace).filter(Workspace.id == fresh.id).first())
        self.assertFalse(old_path.exists())
        self.assertEqual(self.db.query(File).filter(File.workspace_id == old.id).count(), 0)
        self.assertEqual(
            self.db.query(Submission).filter(Submission.workspace_id == old.id).count(), 0
        )

    def test_touch_keeps_workspace_alive(self) -> None:
        ws = self._workspace(_utcnow() - timedelta(days=10))
        touch_workspace(self.db, ws)
        with patch("app.services.workspace.get_settings") as mock_settings:
            mock_settings.return_value = Settings(workspace_ttl_days=7)
            deleted = cleanup_expired_workspaces(self.db)
        self.assertEqual(deleted, 0)
        self.assertIsNotNone(self.db.query(Workspace).filter(Workspace.id == ws.id).first())

    def test_ttl_zero_disables_cleanup(self) -> None:
        self._workspace(_utcnow() - timedelta(days=30))
        with patch("app.services.workspace.get_settings") as mock_settings:
            mock_settings.return_value = Settings(workspace_ttl_days=0)
            deleted = cleanup_expired_workspaces(self.db)
        self.assertEqual(deleted, 0)
        self.assertEqual(self.db.query(Workspace).count(), 1)

    def test_delete_workspace_ignores_missing_disk(self) -> None:
        ws = self._workspace(_utcnow(), disk=False)
        delete_workspace(self.db, ws)
        self.db.commit()
        self.assertEqual(self.db.query(Workspace).count(), 0)


class OpsTokenTests(unittest.TestCase):
    def test_missing_token_is_hidden_404(self) -> None:
        from fastapi.testclient import TestClient

        app = FastAPI()

        @app.post("/internal/seed-exams")
        def seed(request: Request):
            require_ops_token(request)
            return {"ok": True}

        client = TestClient(app)
        with patch("app.api.ops_auth.get_settings", return_value=Settings(cleanup_token="")):
            res = client.post("/internal/seed-exams", json={})
        self.assertEqual(res.status_code, 404, res.text)

    def test_wrong_token_is_403(self) -> None:
        from fastapi.testclient import TestClient

        app = FastAPI()

        @app.post("/internal/seed-exams")
        def seed(request: Request):
            require_ops_token(request)
            return {"ok": True}

        client = TestClient(app)
        with patch(
            "app.api.ops_auth.get_settings",
            return_value=Settings(cleanup_token="secret"),
        ):
            res = client.post("/internal/seed-exams", headers={"X-Cleanup-Token": "nope"}, json={})
        self.assertEqual(res.status_code, 403, res.text)

    def test_matching_token_passes(self) -> None:
        from fastapi.testclient import TestClient

        app = FastAPI()

        @app.post("/internal/seed-exams")
        def seed(request: Request):
            require_ops_token(request)
            return {"ok": True}

        client = TestClient(app)
        with patch(
            "app.api.ops_auth.get_settings",
            return_value=Settings(cleanup_token="secret"),
        ):
            res = client.post("/internal/seed-exams", headers={"X-Cleanup-Token": "secret"}, json={})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json(), {"ok": True})


class EnsureSchemaTests(unittest.TestCase):
    def test_adds_missing_last_accessed_at_column(self) -> None:
        """Postgres production DBs created before this column skip create_all."""
        engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
        with engine.begin() as conn:
            conn.execute(
                text(
                    "CREATE TABLE workspaces ("
                    "id INTEGER PRIMARY KEY, exam_id INTEGER, "
                    "user_id VARCHAR, path VARCHAR)"
                )
            )
        with patch("app.database.engine", engine):
            from app.database import ensure_schema

            ensure_schema()
        cols = {c["name"] for c in inspect(engine).get_columns("workspaces")}
        self.assertIn("last_accessed_at", cols)

    def test_ensure_schema_ddl_includes_column_names(self) -> None:
        import ast
        from pathlib import Path

        src = Path(__file__).resolve().parents[1] / "app" / "database.py"
        tree = ast.parse(src.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            if not isinstance(node.func, ast.Name) or node.func.id != "_add_column_if_missing":
                continue
            args = node.args
            self.assertGreaterEqual(len(args), 3)
            column = ast.literal_eval(args[1])
            ddl = ast.literal_eval(args[2])
            self.assertTrue(
                str(ddl).startswith(str(column) + " "),
                f"ddl {ddl!r} must start with column name {column!r}",
            )


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


if __name__ == "__main__":
    unittest.main()
