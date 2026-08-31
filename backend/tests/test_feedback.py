"""Feedback is stored without analytics consent."""

from __future__ import annotations

import unittest
from unittest.mock import patch

from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.api.feedback import router as feedback_router
from app.config import Settings
from app.database import Base, get_db
from app.models import Feedback
from app.services.rate_limit import RATE_LIMIT_DETAIL, limiter


def _session() -> Session:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()


def _client(db: Session) -> TestClient:
    app = FastAPI()
    app.include_router(feedback_router)

    def _override_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = _override_db
    return TestClient(app)


class FeedbackApiTests(unittest.TestCase):
    def setUp(self) -> None:
        limiter.reset()
        self.db = _session()
        self.client = _client(self.db)
        self._settings = patch(
            "app.api.feedback.get_settings",
            return_value=Settings(posthog_api_key=""),
        )
        self._capture = patch("app.api.feedback.posthog_client.capture")
        self._settings.start()
        self.capture = self._capture.start()

    def tearDown(self) -> None:
        self._capture.stop()
        self._settings.stop()
        limiter.reset()
        self.db.close()

    def test_problem_is_stored_without_visitor_header(self) -> None:
        res = self.client.post(
            "/feedback",
            json={
                "feedback_type": "problem",
                "exam_title": "Virágágyások",
                "task_title": "Beolvasás",
                "message": "A rejtett teszt hibás.",
            },
        )
        self.assertEqual(res.status_code, 200, res.text)
        row_id = res.json()["id"]
        row = self.db.query(Feedback).filter(Feedback.id == row_id).one()
        self.assertEqual(row.feedback_type, "problem")
        self.assertEqual(row.exam_title, "Virágágyások")
        self.assertEqual(row.task_title, "Beolvasás")
        self.assertEqual(row.message, "A rejtett teszt hibás.")

    def test_idea_stores_exam_title_and_blank_task(self) -> None:
        res = self.client.post(
            "/feedback",
            json={
                "feedback_type": "idea",
                "exam_title": "Fogások",
                "message": "Legyen sötét téma.",
            },
        )
        self.assertEqual(res.status_code, 200, res.text)
        row = self.db.query(Feedback).one()
        self.assertEqual(row.feedback_type, "idea")
        self.assertEqual(row.exam_title, "Fogások")
        self.assertEqual(row.task_title, "")
        self.assertEqual(row.message, "Legyen sötét téma.")

    def test_empty_message_rejected(self) -> None:
        res = self.client.post(
            "/feedback",
            json={"feedback_type": "idea", "message": "   "},
        )
        self.assertEqual(res.status_code, 422)

    def test_invalid_type_rejected(self) -> None:
        res = self.client.post(
            "/feedback",
            json={"feedback_type": "other", "message": "hello"},
        )
        self.assertEqual(res.status_code, 422)

    def test_message_too_long_rejected(self) -> None:
        res = self.client.post(
            "/feedback",
            json={"feedback_type": "idea", "message": "x" * 4001},
        )
        self.assertEqual(res.status_code, 422)

    def test_opted_in_visitor_id_is_not_stored(self) -> None:
        res = self.client.post(
            "/feedback",
            json={"feedback_type": "idea", "message": "ok"},
            headers={"X-Visitor-Id": "should-not-persist"},
        )
        self.assertEqual(res.status_code, 200, res.text)
        row = self.db.query(Feedback).one()
        self.assertFalse(hasattr(row, "visitor_id"))

    def test_posthog_capture_uses_anonymous_id_without_visitor_header(self) -> None:
        settings = Settings(posthog_api_key="phc_test", posthog_host="https://eu.i.posthog.com")
        with patch("app.api.feedback.get_settings", return_value=settings):
            res = self.client.post(
                "/feedback",
                json={
                    "feedback_type": "problem",
                    "exam_title": "Demo",
                    "message": "hiba",
                },
            )
        self.assertEqual(res.status_code, 200, res.text)
        self.capture.assert_called_once()
        kwargs = self.capture.call_args.kwargs
        self.assertEqual(kwargs["event"], "feedback_submitted")
        self.assertTrue(str(kwargs["distinct_id"]).startswith("feedback:"))
        self.assertEqual(kwargs["properties"]["feedback_type"], "problem")
        self.assertEqual(kwargs["properties"]["problem"], "hiba")
        self.assertFalse(kwargs["properties"]["$process_person_profile"])

    def test_posthog_capture_uses_visitor_id_when_header_present(self) -> None:
        settings = Settings(posthog_api_key="phc_test")
        with patch("app.api.feedback.get_settings", return_value=settings):
            res = self.client.post(
                "/feedback",
                json={"feedback_type": "idea", "exam_title": "Demo", "message": "ötlet"},
                headers={"X-Visitor-Id": "vid-123"},
            )
        self.assertEqual(res.status_code, 200, res.text)
        kwargs = self.capture.call_args.kwargs
        self.assertEqual(kwargs["distinct_id"], "vid-123")
        self.assertEqual(kwargs["properties"]["feedback"], "ötlet")

    def test_posthog_skipped_without_api_key(self) -> None:
        res = self.client.post(
            "/feedback",
            json={"feedback_type": "idea", "message": "nincs kulcs"},
        )
        self.assertEqual(res.status_code, 200, res.text)
        self.capture.assert_not_called()

    def test_posthog_failure_does_not_lose_the_row(self) -> None:
        settings = Settings(posthog_api_key="phc_test")
        self.capture.side_effect = RuntimeError("down")
        with patch("app.api.feedback.get_settings", return_value=settings):
            res = self.client.post(
                "/feedback",
                json={"feedback_type": "idea", "message": "mégis mentsd"},
            )
        self.assertEqual(res.status_code, 200, res.text)
        self.assertEqual(self.db.query(Feedback).count(), 1)

    def test_list_requires_ops_token(self) -> None:
        with patch("app.api.ops_auth.get_settings", return_value=Settings(cleanup_token="")):
            res = self.client.get("/internal/feedback")
        self.assertEqual(res.status_code, 404)

    def test_list_returns_newest_first(self) -> None:
        self.client.post("/feedback", json={"feedback_type": "idea", "message": "első"})
        self.client.post("/feedback", json={"feedback_type": "idea", "message": "második"})
        with patch(
            "app.api.ops_auth.get_settings",
            return_value=Settings(cleanup_token="secret"),
        ):
            res = self.client.get(
                "/internal/feedback",
                headers={"X-Cleanup-Token": "secret"},
            )
        self.assertEqual(res.status_code, 200, res.text)
        messages = [row["message"] for row in res.json()]
        self.assertEqual(messages, ["második", "első"])


class FeedbackRateLimitTests(unittest.TestCase):
    def setUp(self) -> None:
        limiter.reset()
        self.db = _session()
        self.client = _client(self.db)
        self._settings = patch(
            "app.api.feedback.get_settings",
            return_value=Settings(posthog_api_key=""),
        )
        self._capture = patch("app.api.feedback.posthog_client.capture")
        self._settings.start()
        self._capture.start()

    def tearDown(self) -> None:
        self._capture.stop()
        self._settings.stop()
        limiter.reset()
        self.db.close()

    def test_429_after_limit(self) -> None:
        settings = Settings(rate_limit_feedback_per_minute=1, rate_limit_window_seconds=60)
        with patch("app.services.rate_limit.get_settings", return_value=settings):
            first = self.client.post(
                "/feedback",
                json={"feedback_type": "idea", "message": "egy"},
            )
            second = self.client.post(
                "/feedback",
                json={"feedback_type": "idea", "message": "kettő"},
            )
        self.assertEqual(first.status_code, 200, first.text)
        self.assertEqual(second.status_code, 429)
        self.assertEqual(second.json()["detail"], RATE_LIMIT_DETAIL)
        self.assertEqual(self.db.query(Feedback).count(), 1)


if __name__ == "__main__":
    unittest.main()
