"""Exam template engine.

Templates define dataset files and task types. Expected outputs are always
computed from dataset contents + task builders — never authored separately.
AI may only rewrite story text, never grading rules.
"""

from __future__ import annotations

import json
from typing import Any

from sqlalchemy.orm import Session

from app.exams.builders import expected_for_task, parse_dataset, raw_file_preamble
from app.exams.loader import LoadedExam, load_exam_by_id
from app.models import Exam, ExamFile, Task, TestCase
from app.schemas.templates import ExamTemplate
from app.services import ai_generator


def _task_spec_dict(task: Any) -> dict[str, Any]:
    if hasattr(task, "model_dump"):
        return task.model_dump()
    return dict(task)


def compose_source(exam: Exam, task: Task, student_code: str) -> str:
    """Option A: prepend canonical preamble when the task opts in."""
    code = student_code or ""
    if task.uses_preamble and (exam.preamble or "").strip():
        return exam.preamble.rstrip() + "\n\n" + code
    return code


def materialize_loaded_exam(
    db: Session,
    loaded: LoadedExam,
    *,
    use_ai: bool = False,
) -> Exam:
    """Create DB exam/tasks/tests from a loaded catalog exam."""
    template = loaded.template
    data_file = template.data_file
    dataset_type = template.dataset_type

    story = template.story
    if use_ai:
        story = ai_generator.rewrite_story(
            story or template.description,
            context={"title": template.title, "exam_id": template.id},
        )

    shared_variable = template.shared_variable or "data"
    preamble = (template.preamble or "").strip() or raw_file_preamble(
        template.data_file, shared_variable
    )

    exam = Exam(
        title=template.title,
        description=template.description,
        story=story,
        template_type=template.id,
        preamble=preamble,
        shared_variable=shared_variable,
        level=template.level or "kozep",
        difficulty=int(template.difficulty or 2),
        tags_json=json.dumps(list(template.tags or []), ensure_ascii=False),
        constraints_json=json.dumps(list(template.constraints or []), ensure_ascii=False),
        data_explanation=template.data_explanation or "",
    )
    db.add(exam)
    db.flush()

    db.add(
        ExamFile(
            exam_id=exam.id,
            filename=data_file,
            content=loaded.visible_content,
            read_only=True,
        )
    )

    plugin = loaded.plugin
    visible_rows = parse_dataset(dataset_type, loaded.visible_content, plugin=plugin)
    hidden_rows_list = [
        parse_dataset(dataset_type, content, plugin=plugin) for content in loaded.hidden_contents
    ]

    for idx, task_tmpl in enumerate(template.tasks):
        spec = _task_spec_dict(task_tmpl)
        expected_visible = expected_for_task(visible_rows, spec, plugin=plugin)
        points = int(spec.get("points", 1))
        hints = list(spec.get("hints") or [])
        uses_preamble = bool(spec.get("uses_preamble", False))
        starter = spec.get("starter") or ""
        solution_file = spec.get("solution_file") or f"feladat{idx + 1}.py"
        stdin = spec.get("stdin") or ""
        expected_file = spec.get("expected_file") or ""
        task_tags = list(spec.get("tags") or [])

        task = Task(
            exam_id=exam.id,
            title=spec.get("title") or spec.get("type", "task"),
            description=spec.get("description") or "",
            points=points,
            order_index=idx,
            hints_json=json.dumps(hints, ensure_ascii=False),
            solution_file=solution_file,
            uses_preamble=uses_preamble,
            starter=starter,
            tags_json=json.dumps(task_tags, ensure_ascii=False),
            stdin=stdin,
            expected_file=expected_file,
        )
        db.add(task)
        db.flush()

        db.add(
            ExamFile(
                exam_id=exam.id,
                filename=solution_file,
                content=starter,
                read_only=False,
            )
        )

        db.add(
            TestCase(
                task_id=task.id,
                name=f"{spec.get('type', 'task')}-sample",
                input_files="{}",
                stdin=stdin,
                expected_output=expected_visible,
                is_hidden=False,
                points=points,
            )
        )

        for h_idx, (hidden_content, hidden_rows) in enumerate(
            zip(loaded.hidden_contents, hidden_rows_list), start=1
        ):
            expected_hidden = expected_for_task(hidden_rows, spec, plugin=plugin)
            db.add(
                TestCase(
                    task_id=task.id,
                    name=f"{spec.get('type', 'task')}-hidden-{h_idx:02d}",
                    input_files=json.dumps({data_file: hidden_content}, ensure_ascii=False),
                    stdin=stdin,
                    expected_output=expected_hidden,
                    is_hidden=True,
                    points=points,
                )
            )

    db.commit()
    db.refresh(exam)
    return exam


def create_exam_from_template(
    db: Session,
    template: dict[str, Any] | ExamTemplate | None = None,
    *,
    exam_id: str | None = None,
    use_ai: bool = False,
    seed: int | None = None,
) -> Exam:
    """Materialize an exam from catalog id or an inline template dict."""
    del seed
    if exam_id:
        loaded = load_exam_by_id(exam_id)
        return materialize_loaded_exam(db, loaded, use_ai=use_ai)

    if template is None:
        loaded = load_exam_by_id("cities")
        return materialize_loaded_exam(db, loaded, use_ai=use_ai)

    if isinstance(template, ExamTemplate):
        tmpl = template
    else:
        tmpl = ExamTemplate.model_validate(template)

    try:
        loaded = load_exam_by_id(tmpl.id)
    except FileNotFoundError as exc:
        raise ValueError(
            f"Inline template must match a catalog exam folder (missing: {tmpl.id})"
        ) from exc
    loaded.template = tmpl.model_copy(
        update={
            "visible": loaded.template.visible,
            "hidden": loaded.template.hidden,
            "data_file": loaded.template.data_file,
            "dataset_type": loaded.template.dataset_type,
        }
    )
    return materialize_loaded_exam(db, loaded, use_ai=use_ai)


def default_exam_id() -> str:
    return "cities"
