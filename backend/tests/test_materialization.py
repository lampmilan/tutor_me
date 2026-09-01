"""M1 platform tests: per-test stdin, seed, functions preamble, aux files."""

from __future__ import annotations

import random
import unittest

from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.api import exams as exams_api
from app.database import Base, get_db
from app.exams.builders import build_exam_preamble, expected_for_task
from app.exams.loader import discover_exams, load_exam_by_id, unlisted_catalog_ids
from app.models import Exam, ExamFile, Task, TestCase
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
                    self.assertEqual(exam.origin, loaded.template.origin)
                    self.assertIn(exam.origin, ("official", "synthetic"))
                finally:
                    db.close()


class UnlistedCatalogTests(unittest.TestCase):
    def test_named_exams_are_unlisted_from_the_public_catalog(self) -> None:
        hidden = unlisted_catalog_ids()
        self.assertEqual(
            hidden,
            frozenset(
                {
                    "viragagyasok",
                    "trains",
                    "temperatures",
                    "students",
                    "mrz-kod",
                    "cities",
                }
            ),
        )
        self.assertNotIn("fogasok", hidden)
        self.assertNotIn("versenyido", hidden)

    def test_list_exams_omits_unlisted_but_detail_still_loads(self) -> None:
        engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
        Base.metadata.create_all(engine)
        db = sessionmaker(bind=engine)()
        hidden = Exam(title="Cities", description="", template_type="cities", origin="synthetic")
        visible = Exam(title="Fogások", description="", template_type="fogasok", origin="synthetic")
        official = Exam(title="Létra", description="", template_type="letra", origin="official")
        db.add_all([hidden, visible, official])
        db.commit()
        db.refresh(hidden)
        db.refresh(visible)
        db.refresh(official)

        app = FastAPI()
        app.include_router(exams_api.router)

        def _override_db():
            try:
                yield db
            finally:
                pass

        app.dependency_overrides[get_db] = _override_db
        client = TestClient(app)

        rows = {row["title"]: row for row in client.get("/exams").json()}
        self.assertEqual(set(rows), {"Fogások", "Létra"})
        self.assertEqual(rows["Fogások"]["origin"], "synthetic")
        self.assertEqual(rows["Létra"]["origin"], "official")

        detail = client.get(f"/exams/{hidden.id}")
        self.assertEqual(detail.status_code, 200)
        self.assertEqual(detail.json()["title"], "Cities")
        self.assertEqual(detail.json()["origin"], "synthetic")
        db.close()


class ExamOriginTests(unittest.TestCase):
    def test_catalog_origins_are_official_or_synthetic(self) -> None:
        origins = {loaded.template.id: loaded.template.origin for loaded in discover_exams()}
        self.assertEqual(origins["viragagyasok"], "official")
        for exam_id, origin in origins.items():
            self.assertIn(origin, ("official", "synthetic"), exam_id)
            if exam_id != "viragagyasok":
                self.assertEqual(origin, "synthetic", exam_id)

    def test_invalid_origin_is_rejected(self) -> None:
        from pydantic import ValidationError

        with self.assertRaises(ValidationError):
            ExamTemplate(
                id="demo",
                title="Demo",
                data_file="data.txt",
                dataset_type="lines",
                visible="datasets/visible.txt",
                origin="practice",  # type: ignore[arg-type]
            )

    def test_materialize_copies_origin(self) -> None:
        db = _session()
        official = materialize_loaded_exam(db, load_exam_by_id("viragagyasok"))
        self.assertEqual(official.origin, "official")
        synthetic = materialize_loaded_exam(db, load_exam_by_id("fogasok"))
        self.assertEqual(synthetic.origin, "synthetic")


if __name__ == "__main__":
    unittest.main()
