"""Automatic judging with optional canonical preamble injection (Option A)."""

from __future__ import annotations

import json
from pathlib import Path

from sqlalchemy.orm import Session

from app.models import Exam, File, Submission, Task, Workspace
from app.schemas import JudgeResponse, TestResult
from app.services.executor import execute_python
from app.services.templates import compose_source
from app.services.workspace import sync_workspace_to_disk

GENERIC_GENERALIZATION_HINT = (
    "Your solution works for the example dataset but fails on other datasets."
)
GENERIC_RUNTIME_HINT = "Your program did not finish successfully on every dataset."

# Composed run artifact (preamble + student code). Not shown as a phase file.
RUN_ENTRYPOINT = "main.py"


def _normalize_output(text: str) -> str:
    lines = [line.rstrip() for line in text.replace("\r\n", "\n").replace("\r", "\n").split("\n")]
    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines)


def _task_hints(task: Task) -> list[str]:
    try:
        data = json.loads(task.hints_json or "[]")
    except json.JSONDecodeError:
        return []
    if isinstance(data, list):
        return [str(x) for x in data if str(x).strip()]
    return []


def _collect_hints(
    *,
    sample_passed: bool,
    any_hidden_failed: bool,
    any_runtime_fail: bool,
    failed_task_hints: list[str],
) -> list[str]:
    hints: list[str] = []
    if sample_passed and any_hidden_failed:
        hints.append(GENERIC_GENERALIZATION_HINT)
    if any_runtime_fail:
        hints.append(GENERIC_RUNTIME_HINT)
    for hint in failed_task_hints:
        if hint not in hints:
            hints.append(hint)
    return hints[:3]


def student_code_for_task(workspace: Workspace, task: Task, code: str | None) -> str:
    if code is not None:
        return code
    entry = task.solution_file or "main.py"
    match = next((f for f in workspace.files if f.filename == entry), None)
    if match is not None:
        return match.content
    main = next((f for f in workspace.files if f.filename == "main.py"), None)
    return main.content if main else ""


def prepare_run(
    db: Session,
    workspace: Workspace,
    task: Task,
    student_code: str,
) -> Path:
    """Persist student solution file and write composed source to main.py for execution."""
    exam: Exam = workspace.exam
    composed = compose_source(exam, task, student_code)

    main = next((f for f in workspace.files if f.filename == RUN_ENTRYPOINT), None)
    if main is None:
        main = File(
            workspace_id=workspace.id,
            filename=RUN_ENTRYPOINT,
            content=composed,
            read_only=False,
        )
        db.add(main)
        workspace.files.append(main)
    else:
        main.content = composed

    entry = task.solution_file or RUN_ENTRYPOINT
    if entry != RUN_ENTRYPOINT:
        entry_file = next((f for f in workspace.files if f.filename == entry), None)
        if entry_file is None:
            entry_file = File(
                workspace_id=workspace.id,
                filename=entry,
                content=student_code,
                read_only=False,
            )
            db.add(entry_file)
            workspace.files.append(entry_file)
        else:
            entry_file.content = student_code

    db.commit()
    return sync_workspace_to_disk(workspace)


def judge_workspace(
    db: Session,
    workspace: Workspace,
    *,
    task_id: int | None = None,
    code: str | None = None,
    filename: str | None = None,
) -> JudgeResponse:
    del filename  # solution file comes from the task; kept for API compat
    tasks: list[Task] = list(workspace.exam.tasks)
    if task_id is not None:
        tasks = [t for t in tasks if t.id == task_id]
    tasks = sorted(tasks, key=lambda t: t.order_index)
    if not tasks:
        return JudgeResponse(
            points_earned=0,
            points_possible=0,
            passed_count=0,
            total_count=0,
            summary_line="0/0 tests passed",
            failed_labels=[],
            hints=[],
            results=[],
        )

    results: list[TestResult] = []
    points_earned = 0.0
    points_possible = 0.0
    sample_passed = False
    any_sample_seen = False
    any_hidden_failed = False
    any_runtime_fail = False
    failed_task_hints: list[str] = []
    failed_labels: list[str] = []
    hidden_counter = 0

    for task in tasks:
        student_code = student_code_for_task(workspace, task, code if len(tasks) == 1 else None)
        path = prepare_run(db, workspace, task, student_code)
        cases = sorted(task.test_cases, key=lambda tc: tc.id)

        for tc in cases:
            points_possible += tc.points
            try:
                extra = json.loads(tc.input_files or "{}")
            except json.JSONDecodeError:
                extra = {}

            if tc.is_hidden:
                hidden_counter += 1
                label = f"Hidden Test #{hidden_counter}"
            else:
                label = f"Sample · {task.title}"

            exec_result = execute_python(
                path,
                entrypoint=RUN_ENTRYPOINT,
                stdin=tc.stdin or "",
                extra_files=extra or None,
            )
            actual = _normalize_output(exec_result.output)
            expected = _normalize_output(tc.expected_output)
            runtime_ok = exec_result.exit_code == 0
            passed = actual == expected and runtime_ok
            earned = tc.points if passed else 0
            points_earned += earned

            if not tc.is_hidden:
                any_sample_seen = True
                if passed:
                    sample_passed = True
            elif not passed:
                any_hidden_failed = True

            if not passed and not runtime_ok:
                any_runtime_fail = True

            if not passed:
                failed_labels.append(label)
                for hint in _task_hints(task):
                    if hint not in failed_task_hints:
                        failed_task_hints.append(hint)

            if tc.is_hidden:
                error_msg = ""
                if not passed:
                    if not runtime_ok:
                        error_msg = "Runtime error" if exec_result.exit_code != 124 else "Timed out"
                    else:
                        error_msg = "Wrong answer"
                results.append(
                    TestResult(
                        test_case_id=tc.id,
                        task_id=task.id,
                        name=tc.name,
                        label=label,
                        passed=passed,
                        points_earned=earned,
                        points_possible=tc.points,
                        expected=None,
                        actual=None,
                        error=error_msg,
                        runtime=exec_result.runtime,
                        is_hidden=True,
                    )
                )
            else:
                error_msg = ""
                if not passed:
                    error_msg = exec_result.error or (
                        "Wrong answer" if runtime_ok else f"Exit code {exec_result.exit_code}"
                    )
                results.append(
                    TestResult(
                        test_case_id=tc.id,
                        task_id=task.id,
                        name=tc.name,
                        label=label,
                        passed=passed,
                        points_earned=earned,
                        points_possible=tc.points,
                        expected=expected,
                        actual=actual,
                        error=error_msg,
                        runtime=exec_result.runtime,
                        is_hidden=False,
                    )
                )

    hints = _collect_hints(
        sample_passed=sample_passed and any_sample_seen,
        any_hidden_failed=any_hidden_failed,
        any_runtime_fail=any_runtime_fail,
        failed_task_hints=failed_task_hints,
    )
    passed_count = sum(1 for r in results if r.passed)
    total_count = len(results)
    summary_line = f"{passed_count}/{total_count} tests passed"

    submission = Submission(
        workspace_id=workspace.id,
        task_id=task_id,
        points_earned=points_earned,
        points_possible=points_possible,
        result_json=json.dumps(
            {
                "summary_line": summary_line,
                "hints": hints,
                "results": [r.model_dump() for r in results],
            },
            ensure_ascii=False,
        ),
    )
    db.add(submission)
    db.commit()

    return JudgeResponse(
        points_earned=points_earned,
        points_possible=points_possible,
        passed_count=passed_count,
        total_count=total_count,
        summary_line=summary_line,
        failed_labels=failed_labels,
        hints=hints,
        results=results,
    )
