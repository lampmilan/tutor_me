"""Startup seed should insert missing exams only, not rematerialize the catalog."""

from __future__ import annotations

import unittest
from unittest.mock import patch

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.database import Base
from app.exams.loader import load_exam_by_id
from app.models import Exam
from app.seed import seed_all_exams
from app.services.templates import materialize_loaded_exam


def _session() -> Session:
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()


class SeedMissingOnlyTests(unittest.TestCase):
    def test_startup_seed_skips_existing_without_delete(self) -> None:
        db = _session()
        loaded = load_exam_by_id("fogasok")
        first = materialize_loaded_exam(db, loaded, use_ai=False)
        first_id = first.id
        first.preamble = "# stale on purpose\n"
        db.commit()

        with patch("app.seed.discover_exams", return_value=[loaded]):
            created = seed_all_exams(db, rematerialize=False)

        self.assertEqual(created, [])
        kept = db.query(Exam).filter(Exam.id == first_id).one()
        self.assertTrue(kept.preamble.startswith("# stale on purpose"))

    def test_startup_seed_inserts_missing_catalog_id(self) -> None:
        db = _session()
        loaded = load_exam_by_id("fogasok")
        with patch("app.seed.discover_exams", return_value=[loaded]):
            created = seed_all_exams(db, rematerialize=False)
        self.assertEqual(len(created), 1)
        self.assertEqual(created[0].template_type, "fogasok")

    def test_full_seed_rematerializes_stale_exam(self) -> None:
        db = _session()
        loaded = load_exam_by_id("fogasok")
        first = materialize_loaded_exam(db, loaded, use_ai=False)
        first.preamble = "# stale\n"
        db.commit()

        with patch("app.seed.discover_exams", return_value=[loaded]):
            created = seed_all_exams(db, rematerialize=True)

        self.assertEqual(len(created), 1)
        self.assertEqual(db.query(Exam).count(), 1)
        self.assertFalse((created[0].preamble or "").startswith("# stale"))

    def test_full_seed_rematerializes_when_origin_changes(self) -> None:
        db = _session()
        loaded = load_exam_by_id("fogasok")
        first = materialize_loaded_exam(db, loaded, use_ai=False)
        first.origin = "official"
        db.commit()

        with patch("app.seed.discover_exams", return_value=[loaded]):
            created = seed_all_exams(db, rematerialize=True)

        self.assertEqual(len(created), 1)
        self.assertEqual(created[0].origin, "synthetic")
        self.assertEqual(db.query(Exam).count(), 1)


if __name__ == "__main__":
    unittest.main()
