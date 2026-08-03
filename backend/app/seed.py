"""Seed all catalog exams from backend/app/exams/*/template.json."""

from sqlalchemy.orm import Session, joinedload

from app.exams.loader import discover_exams
from app.models import Exam, Task
from app.services.templates import materialize_loaded_exam


def _hidden_test_count(exam: Exam) -> int:
    return sum(1 for task in exam.tasks for tc in task.test_cases if tc.is_hidden)


def seed_all_exams(db: Session) -> list[Exam]:
    """Materialize each catalog exam once.

    If an older seed exists without hidden tests, replace it so Submit
    gets the LeetCode-style hidden evaluation layout.
    """
    created: list[Exam] = []
    for loaded in discover_exams():
        expected_hidden = len(loaded.hidden_contents) * len(loaded.template.tasks)
        existing = (
            db.query(Exam)
            .options(joinedload(Exam.tasks).joinedload(Task.test_cases))
            .filter(
                (Exam.template_type == loaded.template.id)
                | (Exam.title == loaded.template.title)
            )
            .first()
        )
        if existing and _hidden_test_count(existing) >= expected_hidden:
            created.append(existing)
            continue
        if existing:
            db.delete(existing)
            db.commit()

        exam = materialize_loaded_exam(db, loaded, use_ai=False)
        created.append(exam)
    return created


def seed_cities_exam(db: Session) -> Exam | None:
    """Back-compat alias."""
    exams = seed_all_exams(db)
    for exam in exams:
        if exam.title == "Cities":
            return exam
    return exams[0] if exams else None
