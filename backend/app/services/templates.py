"""Exam template engine.

Templates define dataset files and task types. Expected outputs are always
computed from dataset contents + task builders — never authored separately.
AI may only rewrite story text, never grading rules.
"""

from __future__ import annotations

import json
from typing import Any

from sqlalchemy.orm import Session

from app.exams.builders import build_exam_preamble, expected_for_task, parse_dataset
from app.exams.loader import LoadedExam, load_exam_by_id
from app.models import Exam, ExamFile, Task, TestCase
from app.schemas.templates import ExamTemplate
from app.services import ai_generator


def _task_spec_dict(task: Any) -> dict[str, Any]:
    if hasattr(task, "model_dump"):
        return task.model_dump()
    return dict(task)


def _stdin_for_case(spec: dict[str, Any], *, hidden_index: int | None = None) -> str:
    """Resolve stdin for sample (hidden_index=None) or a hidden test case."""
    if hidden_index is not None:
        hidden_stdin = list(spec.get("hidden_stdin") or [])
        if hidden_index < len(hidden_stdin):
            return hidden_stdin[hidden_index] or ""
    return spec.get("stdin") or ""


def _effective_seed(template: Any, override: int | None = None) -> int | None:
    if override is not None:
        return override
    return getattr(template, "seed", None)


def _data_file_for_exam(exam: Exam) -> str:
    """Resolve the mounted dataset filename for store-load checks."""
    name = (getattr(exam, "data_file", None) or "").strip()
    if name:
        return name
    preamble = exam.preamble or ""
    marker = 'open("'
    start = preamble.find(marker)
    if start >= 0:
        start += len(marker)
        end = preamble.find('"', start)
        if end > start:
            return preamble[start:end]
    return ""


def store_load_epilogue(shared_variable: str, data_file: str) -> str:
    """Runtime check: student must leave shared_variable equal to the data file."""
    var = shared_variable or "data"
    path = data_file or "data.txt"
    return (
        "\n\n# --- VizsgaGO beolvasás ellenőrzés ---\n"
        f"try:\n"
        f"    __vg_actual = {var}\n"
        f"except NameError as __vg_exc:\n"
        f"    raise SystemExit(\"A '{var}' változó nincs definiálva.\") from __vg_exc\n"
        f"with open({path!r}, encoding=\"utf-8\") as __vg_f:\n"
        f"    __vg_expected = __vg_f.read()\n"
        f"if __vg_actual != __vg_expected:\n"
        f"    raise SystemExit(\n"
        f"        \"A '{var}' változó nem a(z) '{path}' fájl tartalmát tartalmazza.\"\n"
        f"    )\n"
    )


def should_verify_store_load(task: Task) -> bool:
    """File-load store feladats only (not function stubs / spec-only store rows)."""
    if getattr(task, "verify_store_load", False):
        return True
    # After rematerialize, task_type is set and verify_store_load is authoritative.
    if (getattr(task, "task_type", None) or "").strip():
        return False
    # Legacy DB fallback: graded store tasks have store-sample / store-hidden-* cases.
    if task.uses_preamble:
        return False
    return any((tc.name or "").startswith("store-") for tc in (task.test_cases or []))


def compose_source(exam: Exam, task: Task, student_code: str) -> str:
    """Option A: prepend canonical preamble when the task opts in.

    For file-load ``store`` feladats, append a check that ``shared_variable``
    equals the mounted data file so empty/wrong solutions no longer auto-pass.
    """
    code = student_code or ""
    if task.uses_preamble and (exam.preamble or "").strip():
        code = exam.preamble.rstrip() + "\n\n" + code
    if should_verify_store_load(task):
        data_file = _data_file_for_exam(exam)
        shared = exam.shared_variable or "data"
        if data_file and shared:
            code = code.rstrip() + store_load_epilogue(shared, data_file)
    return code


def materialize_loaded_exam(
    db: Session,
    loaded: LoadedExam,
    *,
    use_ai: bool = False,
    seed_override: int | None = None,
) -> Exam:
    """Create DB exam/tasks/tests from a loaded catalog exam."""
    template = loaded.template
    data_file = template.data_file
    dataset_type = template.dataset_type
    seed = _effective_seed(template, seed_override)

    story = template.story
    if use_ai:
        story = ai_generator.rewrite_story(
            story or template.description,
            context={"title": template.title, "exam_id": template.id},
        )

    shared_variable = template.shared_variable or "data"
    preamble = build_exam_preamble(template)

    exam = Exam(
        title=template.title,
        description=template.description,
        story=story,
        template_type=template.id,
        preamble=preamble,
        shared_variable=shared_variable,
        data_file=data_file,
        level=template.level or "kozep",
        origin=template.origin or "synthetic",
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

    for aux in template.aux_files or []:
        db.add(
            ExamFile(
                exam_id=exam.id,
                filename=aux.filename,
                content=aux.content,
                read_only=aux.read_only,
            )
        )

    plugin = loaded.plugin
    visible_rows = parse_dataset(dataset_type, loaded.visible_content, plugin=plugin)
    hidden_rows_list = [
        parse_dataset(dataset_type, content, plugin=plugin) for content in loaded.hidden_contents
    ]
    created_solution_files: set[str] = set()
    # Store feladats that share a later graded .py are spec-only (no own tests).
    gradeable_files: set[str] = set()
    for i, t in enumerate(template.tasks):
        s = _task_spec_dict(t)
        if s.get("type") != "store":
            gradeable_files.add(s.get("solution_file") or f"feladat{i + 1}.py")

    for idx, task_tmpl in enumerate(template.tasks):
        spec = _task_spec_dict(task_tmpl)
        sample_stdin = _stdin_for_case(spec)
        spec_with_stdin = {**spec, "stdin": sample_stdin}
        expected_visible = expected_for_task(
            visible_rows, spec_with_stdin, plugin=plugin, seed=seed
        )
        points = int(spec.get("points", 1))
        hints = list(spec.get("hints") or [])
        uses_preamble = bool(spec.get("uses_preamble", False))
        starter = spec.get("starter") or ""
        solution_file = spec.get("solution_file") or f"feladat{idx + 1}.py"
        stdin = sample_stdin
        expected_file = spec.get("expected_file") or ""
        task_tags = list(spec.get("tags") or [])
        task_type = str(spec.get("type") or "")
        # Own-file store + no preamble ⇒ student must actually read the data file.
        store_is_spec_only = task_type == "store" and solution_file in gradeable_files
        verify_store_load = (
            task_type == "store" and not uses_preamble and not store_is_spec_only
        )

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
            task_type=task_type,
            verify_store_load=verify_store_load,
        )
        db.add(task)
        db.flush()

        # One workspace file per name: later feladats may share a monolith .py.
        if solution_file not in created_solution_files:
            db.add(
                ExamFile(
                    exam_id=exam.id,
                    filename=solution_file,
                    content=starter,
                    read_only=False,
                )
            )
            created_solution_files.add(solution_file)

        if store_is_spec_only:
            continue

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
            hidden_stdin = _stdin_for_case(spec, hidden_index=h_idx - 1)
            spec_hidden = {**spec, "stdin": hidden_stdin}
            expected_hidden = expected_for_task(
                hidden_rows, spec_hidden, plugin=plugin, seed=seed
            )
            db.add(
                TestCase(
                    task_id=task.id,
                    name=f"{spec.get('type', 'task')}-hidden-{h_idx:02d}",
                    input_files=json.dumps({data_file: hidden_content}, ensure_ascii=False),
                    stdin=hidden_stdin,
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
    if exam_id:
        loaded = load_exam_by_id(exam_id)
        return materialize_loaded_exam(db, loaded, use_ai=use_ai, seed_override=seed)

    if template is None:
        loaded = load_exam_by_id("cities")
        return materialize_loaded_exam(db, loaded, use_ai=use_ai, seed_override=seed)

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
    effective_seed = seed if seed is not None else tmpl.seed
    loaded.template = tmpl.model_copy(
        update={
            "visible": loaded.template.visible,
            "hidden": loaded.template.hidden,
            "data_file": loaded.template.data_file,
            "dataset_type": loaded.template.dataset_type,
            "seed": effective_seed,
        }
    )
    return materialize_loaded_exam(db, loaded, use_ai=use_ai, seed_override=seed)


def default_exam_id() -> str:
    return "cities"
