"""File-load store feladats must not auto-pass on empty/wrong solutions."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, joinedload, sessionmaker

from app.config import Settings
from app.database import Base
from app.exams.loader import load_exam_by_id
from app.models import Exam, Task, Workspace
from app.services.judge import judge_workspace, prepare_run
from app.services.templates import (
    compose_source,
    materialize_loaded_exam,
    should_verify_store_load,
    store_load_epilogue,
)
from app.services.workspace import create_workspace


def _session() -> Session:
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()


class StoreLoadEpilogueTests(unittest.TestCase):
    def test_epilogue_asserts_shared_variable(self) -> None:
        snippet = store_load_epilogue("fogasok", "fogasok.txt")
        self.assertIn("fogasok", snippet)
        self.assertIn("fogasok.txt", snippet)
        self.assertIn("SystemExit", snippet)

    def test_fogasok_beolvasas_gets_verify_flag(self) -> None:
        db = _session()
        exam = materialize_loaded_exam(db, load_exam_by_id("fogasok"))
        self.assertEqual(exam.data_file, "fogasok.txt")
        task = (
            db.query(Task)
            .filter(Task.exam_id == exam.id, Task.title == "1. feladat: Beolvasás")
            .one()
        )
        self.assertEqual(task.task_type, "store")
        self.assertTrue(task.verify_store_load)
        self.assertTrue(should_verify_store_load(task))
        composed = compose_source(exam, task, 'fogasok = ""\n')
        self.assertIn("VizsgaGO beolvasás ellenőrzés", composed)
        self.assertIn("fogasok.txt", composed)

    def test_szolanc_spec_only_store_not_verified(self) -> None:
        db = _session()
        exam = materialize_loaded_exam(db, load_exam_by_id("szolanc"))
        task = (
            db.query(Task)
            .filter(Task.exam_id == exam.id, Task.title == "Szavak bekérése")
            .one()
        )
        self.assertEqual(task.task_type, "store")
        self.assertFalse(task.verify_store_load)
        self.assertFalse(should_verify_store_load(task))
        composed = compose_source(exam, task, task.starter)
        self.assertNotIn("VizsgaGO beolvasás ellenőrzés", composed)

    def test_function_store_with_preamble_not_verified(self) -> None:
        db = _session()
        exam = materialize_loaded_exam(db, load_exam_by_id("golya"))
        task = db.query(Task).filter(Task.exam_id == exam.id, Task.title == "tavolsag").one()
        self.assertEqual(task.task_type, "store")
        self.assertTrue(task.uses_preamble)
        self.assertFalse(task.verify_store_load)
        self.assertFalse(should_verify_store_load(task))


class StoreLoadJudgeTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmpdir.cleanup)
        self.db = _session()
        self._settings = Settings(workspaces_root=self._tmpdir.name)

    def _workspace_for_fogasok(self) -> Workspace:
        exam = materialize_loaded_exam(self.db, load_exam_by_id("fogasok"))
        with patch("app.services.workspace.get_settings", return_value=self._settings):
            workspace = create_workspace(self.db, exam, user_id="test-store")
        # Attach fully loaded exam graph the way the judge API does.
        workspace.exam = (
            self.db.query(Exam)
            .options(joinedload(Exam.tasks).joinedload(Task.test_cases))
            .filter(Exam.id == exam.id)
            .one()
        )
        return workspace

    def test_incorrect_literal_fails_store_task(self) -> None:
        workspace = self._workspace_for_fogasok()
        task = next(t for t in workspace.exam.tasks if t.verify_store_load)
        bad = 'fogasok = "THIS SHOULD BE INCORRECT"\n'
        with patch("app.services.workspace.get_settings", return_value=self._settings):
            result = judge_workspace(self.db, workspace, task_id=task.id, code=bad)
        self.assertEqual(result.passed_count, 0)
        self.assertGreater(result.total_count, 0)
        self.assertTrue(all(not r.passed for r in result.results))

    def test_empty_starter_fails_store_task(self) -> None:
        workspace = self._workspace_for_fogasok()
        task = next(t for t in workspace.exam.tasks if t.verify_store_load)
        with patch("app.services.workspace.get_settings", return_value=self._settings):
            result = judge_workspace(
                self.db, workspace, task_id=task.id, code='fogasok = ""\n'
            )
        self.assertEqual(result.passed_count, 0)

    def test_correct_open_read_passes_store_task(self) -> None:
        workspace = self._workspace_for_fogasok()
        task = next(t for t in workspace.exam.tasks if t.verify_store_load)
        good = (
            'with open("fogasok.txt", encoding="utf-8") as f:\n'
            "    fogasok = f.read()\n"
        )
        with patch("app.services.workspace.get_settings", return_value=self._settings):
            result = judge_workspace(self.db, workspace, task_id=task.id, code=good)
        self.assertEqual(result.passed_count, result.total_count)
        self.assertGreater(result.total_count, 0)
        self.assertTrue(all(r.passed for r in result.results))

    def test_prepare_run_writes_epilogue_into_main(self) -> None:
        workspace = self._workspace_for_fogasok()
        task = next(t for t in workspace.exam.tasks if t.verify_store_load)
        with patch("app.services.workspace.get_settings", return_value=self._settings):
            path = prepare_run(self.db, workspace, task, 'fogasok = ""\n')
        main = Path(path) / "main.py"
        self.assertTrue(main.is_file())
        text = main.read_text(encoding="utf-8")
        self.assertIn("VizsgaGO beolvasás ellenőrzés", text)


if __name__ == "__main__":
    unittest.main()
