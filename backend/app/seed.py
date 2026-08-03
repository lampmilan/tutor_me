"""Seed all catalog exams from backend/app/exams/*/template.json."""

from sqlalchemy.orm import Session, joinedload

from app.exams.loader import discover_exams
from app.models import Exam, Task
from app.services.templates import materialize_loaded_exam


def _hidden_test_count(exam: Exam) -> int:
    return sum(1 for task in exam.tasks for tc in task.test_cases if tc.is_hidden)


def _needs_phase_upgrade(exam: Exam, loaded) -> bool:
    """True when exam lacks per-task solution files from the current template."""
    expected_files = {
        (t.solution_file or f"feladat_{i + 1}.py")
        for i, t in enumerate(loaded.template.tasks)
    }
    if not expected_files:
        return False
    existing_names = {f.filename for f in exam.files}
    if not expected_files.issubset(existing_names):
        return True
    if len(exam.tasks) != len(loaded.template.tasks):
        return True
    by_order = sorted(exam.tasks, key=lambda t: t.order_index)
    for task, tmpl in zip(by_order, loaded.template.tasks):
        want = tmpl.solution_file or None
        if want and getattr(task, "solution_file", None) != want:
            return True
        if not getattr(task, "solution_file", None) or task.solution_file == "main.py":
            if want:
                return True
    return False


def seed_all_exams(db: Session) -> list[Exam]:
    """Materialize each catalog exam once.

    Re-seeds when hidden tests are missing or phase solution files are absent.
    """
    created: list[Exam] = []
    for loaded in discover_exams():
        expected_hidden = len(loaded.hidden_contents) * len(loaded.template.tasks)
        existing = (
            db.query(Exam)
            .options(
                joinedload(Exam.files),
                joinedload(Exam.tasks).joinedload(Task.test_cases),
            )
            .filter(
                (Exam.template_type == loaded.template.id)
                | (Exam.title == loaded.template.title)
            )
            .first()
        )
        if (
            existing
            and _hidden_test_count(existing) >= expected_hidden
            and not _needs_phase_upgrade(existing, loaded)
        ):
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
