"""M1 platform tests: per-test stdin, seed, functions preamble, aux files."""

from __future__ import annotations

import random
import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.database import Base
from app.exams.builders import build_exam_preamble, expected_for_task
from app.exams.loader import discover_exams, load_exam_by_id
from app.models import ExamFile, Task, TestCase
from app.schemas.templates import AuxFileTemplate, ExamTemplate, TaskTemplate
from app.services.templates import materialize_loaded_exam


def _session() -> Session:
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()


class PreambleTests(unittest.TestCase):
    def test_build_preamble_includes_seed_functions_and_load(self) -> None:
        tmpl = ExamTemplate(
            id="demo",
            title="Demo",
            data_file="data.txt",
            dataset_type="lines",
            visible="datasets/visible.txt",
            shared_variable="data",
            seed=42,
            functions="def percben(perc: int) -> int:\n    return perc // 60",
        )
        preamble = build_exam_preamble(tmpl)
        self.assertIn("import random", preamble)
        self.assertIn("random.seed(42)", preamble)
        self.assertIn('open("data.txt"', preamble)
        self.assertIn("def percben", preamble)

    def test_seed_produces_deterministic_random_in_oracle(self) -> None:
        def _random_pick(_rows, _spec):
            return str(random.randint(1, 1000))

        import app.exams.builders as builders

        builders.TASK_BUILDERS["_test_random_pick"] = _random_pick
        try:
            first = expected_for_task([], {"type": "_test_random_pick"}, seed=99)
            second = expected_for_task([], {"type": "_test_random_pick"}, seed=99)
            third = expected_for_task([], {"type": "_test_random_pick"}, seed=100)
            self.assertEqual(first, second)
            self.assertNotEqual(first, third)
        finally:
            del builders.TASK_BUILDERS["_test_random_pick"]


class MaterializationTests(unittest.TestCase):
    def test_per_hidden_stdin_materializes_distinct_test_cases(self) -> None:
        db = _session()
        loaded = load_exam_by_id("cities")
        loaded.template = loaded.template.model_copy(
            update={
                "tasks": [
                    TaskTemplate(
                        type="literal",
                        title="Interactive",
                        value="sample",
                        stdin="A\n",
                        hidden_stdin=["X\n", "Y\n"],
                    )
                ]
            }
        )
        loaded.hidden_contents = ["Budapest 1\n", "Szeged 2\n"]
        exam = materialize_loaded_exam(db, loaded)
        task = db.query(Task).filter(Task.exam_id == exam.id).one()
        cases = (
            db.query(TestCase)
            .filter(TestCase.task_id == task.id)
            .order_by(TestCase.is_hidden, TestCase.name)
            .all()
        )
        self.assertEqual(len(cases), 3)
        self.assertEqual(cases[0].stdin, "A\n")
        self.assertFalse(cases[0].is_hidden)
        self.assertEqual(cases[1].stdin, "X\n")
        self.assertTrue(cases[1].is_hidden)
        self.assertEqual(cases[2].stdin, "Y\n")
        self.assertTrue(cases[2].is_hidden)
        self.assertNotEqual(cases[1].stdin, cases[2].stdin)

    def test_aux_files_materialize_as_read_only_exam_files(self) -> None:
        db = _session()
        loaded = load_exam_by_id("cities")
        loaded.template = loaded.template.model_copy(
            update={
                "aux_files": [
                    AuxFileTemplate(
                        filename="kodok.txt",
                        content="A 1\nB 2\n",
                        read_only=True,
                    )
                ],
                "tasks": [TaskTemplate(type="count", title="Count", field=None)],
            }
        )
        exam = materialize_loaded_exam(db, loaded)
        aux = (
            db.query(ExamFile)
            .filter(ExamFile.exam_id == exam.id, ExamFile.filename == "kodok.txt")
            .one()
        )
        self.assertTrue(aux.read_only)
        self.assertIn("A 1", aux.content)

    def test_viragagyasok_bed_query_hidden_stdin_differs(self) -> None:
        db = _session()
        loaded = load_exam_by_id("viragagyasok")
        exam = materialize_loaded_exam(db, loaded)
        task = (
            db.query(Task)
            .filter(Task.exam_id == exam.id, Task.title == "Egy ágyás")
            .one()
        )
        hidden = (
            db.query(TestCase)
            .filter(TestCase.task_id == task.id, TestCase.is_hidden.is_(True))
            .order_by(TestCase.name)
            .all()
        )
        self.assertEqual(len(hidden), 3)
        stdins = [tc.stdin for tc in hidden]
        self.assertEqual(stdins, ["1\n", "100\n", "50\n"])
        self.assertEqual(len(set(stdins)), 3)


class MaterializeAllCatalogTests(unittest.TestCase):
    """Verify that every catalog exam can be materialized without error (M5 CI gate)."""

    def test_every_catalog_exam_materializes_without_error(self) -> None:
        exams = discover_exams()
        self.assertGreaterEqual(len(exams), 20, "Expected at least 20 catalog exams")
        for loaded in exams:
            with self.subTest(exam=loaded.template.id):
                db = _session()
                try:
                    exam = materialize_loaded_exam(db, loaded)
                    self.assertIsNotNone(exam.id)
                    self.assertEqual(exam.template_type, loaded.template.id)
                finally:
                    db.close()


if __name__ == "__main__":
    unittest.main()
