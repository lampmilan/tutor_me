"""Seed all catalog exams from backend/app/exams/*/template.json."""

from sqlalchemy.orm import Session, joinedload

from app.exams.loader import discover_exams
from app.models import Exam, Task
from app.services.templates import materialize_loaded_exam


def _needs_rematerialize(exam: Exam, loaded, expected_hidden: int) -> bool:
    hidden = sum(1 for task in exam.tasks for tc in task.test_cases if tc.is_hidden)
    if hidden < expected_hidden:
        return True
    if not (exam.preamble or "").strip() and (loaded.template.preamble or "").strip():
        return True
    if len(exam.tasks) != len(loaded.template.tasks):
        return True
    expected_files = {
        (t.solution_file or f"feladat{i + 1}.py")
        for i, t in enumerate(loaded.template.tasks)
    }
    existing_names = {f.filename for f in exam.files}
    if expected_files and not expected_files.issubset(existing_names):
        return True
    by_order = sorted(exam.tasks, key=lambda t: t.order_index)
    for task, tmpl in zip(by_order, loaded.template.tasks):
        want = tmpl.solution_file or None
        if want and getattr(task, "solution_file", None) != want:
            return True
        if bool(getattr(task, "uses_preamble", False)) != bool(tmpl.uses_preamble):
            return True
    return False


def seed_all_exams(db: Session) -> list[Exam]:
    """Materialize each catalog exam once (rematerialize if outdated)."""
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
        if existing and not _needs_rematerialize(existing, loaded, expected_hidden):
            created.append(existing)
            continue
        if existing:
            db.delete(existing)
            db.commit()

        exam = materialize_loaded_exam(db, loaded, use_ai=False)
        created.append(exam)
    return created


def seed_cities_exam(db: Session) -> Exam | None:
    exams = seed_all_exams(db)
    for exam in exams:
        if exam.title == "Cities":
            return exam
    return exams[0] if exams else None
