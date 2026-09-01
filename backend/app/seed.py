"""Seed all catalog exams from backend/app/exams/*/template.json."""

import json

from sqlalchemy.orm import Session, joinedload

from app.exams.builders import build_exam_preamble
from app.exams.loader import discover_exams
from app.models import Exam, Task
from app.services.templates import materialize_loaded_exam


def _json_list(raw: str | None) -> list:
    try:
        data = json.loads(raw or "[]")
    except json.JSONDecodeError:
        return []
    return data if isinstance(data, list) else []


def _needs_rematerialize(exam: Exam, loaded, expected_hidden: int) -> bool:
    hidden = sum(1 for task in exam.tasks for tc in task.test_cases if tc.is_hidden)
    if hidden < expected_hidden:
        return True
    want_preamble = build_exam_preamble(loaded.template).strip()
    if (exam.preamble or "").strip() != want_preamble:
        return True
    if (getattr(exam, "shared_variable", None) or "data") != (
        loaded.template.shared_variable or "data"
    ):
        return True
    if len(exam.tasks) != len(loaded.template.tasks):
        return True
    expected_files = {
        (t.solution_file or f"feladat{i + 1}.py")
        for i, t in enumerate(loaded.template.tasks)
    }
    expected_files.add(loaded.template.data_file)
    for aux in loaded.template.aux_files or []:
        expected_files.add(aux.filename)
    existing_names = {f.filename for f in exam.files}
    if expected_files and not expected_files.issubset(existing_names):
        return True
    if (getattr(exam, "level", None) or "kozep") != (loaded.template.level or "kozep"):
        return True
    if (getattr(exam, "origin", None) or "synthetic") != (loaded.template.origin or "synthetic"):
        return True
    if int(getattr(exam, "difficulty", 0) or 0) != int(loaded.template.difficulty or 0):
        return True
    if _json_list(getattr(exam, "tags_json", None)) != list(loaded.template.tags or []):
        return True
    if (getattr(exam, "data_explanation", None) or "") != (loaded.template.data_explanation or ""):
        return True
    by_order = sorted(exam.tasks, key=lambda t: t.order_index)
    for task, tmpl in zip(by_order, loaded.template.tasks):
        want = tmpl.solution_file or None
        if want and getattr(task, "solution_file", None) != want:
            return True
        if (getattr(task, "starter", None) or "") != (tmpl.starter or ""):
            return True
        if bool(getattr(task, "uses_preamble", False)) != bool(tmpl.uses_preamble):
            return True
        if _json_list(getattr(task, "tags_json", None)) != list(tmpl.tags or []):
            return True
        if (getattr(task, "stdin", None) or "") != (tmpl.stdin or ""):
            return True
        if (getattr(task, "expected_file", None) or "") != (tmpl.expected_file or ""):
            return True
        hidden_cases = sorted(
            (tc for tc in task.test_cases if tc.is_hidden),
            key=lambda tc: tc.name,
        )
        want_hidden_stdin = list(tmpl.hidden_stdin or [])
        for h_idx, tc in enumerate(hidden_cases):
            want_stdin = (
                want_hidden_stdin[h_idx]
                if h_idx < len(want_hidden_stdin)
                else (tmpl.stdin or "")
            )
            if (tc.stdin or "") != (want_stdin or ""):
                return True
    return False


def seed_all_exams(db: Session, *, rematerialize: bool = True) -> list[Exam]:
    """Materialize each catalog exam once.

    ``rematerialize=False`` (API startup): insert missing catalog ids only.
    Skip the joinedload + stale-check so a warm Neon DB does not block
    Cloud Run from serving the first student request.
    """
    created: list[Exam] = []
    known = db.query(Exam.id, Exam.template_type, Exam.title).all()
    by_type = {template_type: exam_id for exam_id, template_type, _ in known if template_type}
    by_title = {title: exam_id for exam_id, _, title in known}

    for loaded in discover_exams():
        existing_id = by_type.get(loaded.template.id) or by_title.get(loaded.template.title)
        if existing_id is not None and not rematerialize:
            continue

        existing = None
        if existing_id is not None:
            existing = (
                db.query(Exam)
                .options(
                    joinedload(Exam.files),
                    joinedload(Exam.tasks).joinedload(Task.test_cases),
                )
                .filter(Exam.id == existing_id)
                .first()
            )

        expected_hidden = len(loaded.hidden_contents) * len(loaded.template.tasks)
        if existing and not _needs_rematerialize(existing, loaded, expected_hidden):
            created.append(existing)
            continue
        if existing:
            db.delete(existing)
            db.commit()

        exam = materialize_loaded_exam(db, loaded, use_ai=False)
        created.append(exam)
        by_type[loaded.template.id] = exam.id
        by_title[loaded.template.title] = exam.id
    return created


def seed_cities_exam(db: Session) -> Exam | None:
    exams = seed_all_exams(db)
    for exam in exams:
        if exam.title == "Cities":
            return exam
    return exams[0] if exams else None
