"""Automatic judging: run student code against test cases and award points."""

from __future__ import annotations

import json

from sqlalchemy.orm import Session

from app.models import File, Submission, Task, TestCase, Workspace
from app.schemas import JudgeResponse, TestResult
from app.services.executor import execute_python
from app.services.workspace import sync_workspace_to_disk


def _normalize_output(text: str) -> str:
    """Normalize whitespace for comparison (érettségi-friendly)."""
    lines = [line.rstrip() for line in text.replace("\r\n", "\n").replace("\r", "\n").split("\n")]
    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines)


def judge_workspace(
    db: Session,
    workspace: Workspace,
    *,
    task_id: int | None = None,
    code: str | None = None,
) -> JudgeResponse:
    if code is not None:
        main = next((f for f in workspace.files if f.filename == "main.py"), None)
        if main is None:
            main = File(workspace_id=workspace.id, filename="main.py", content=code, read_only=False)
            db.add(main)
            workspace.files.append(main)
        else:
            main.content = code
        db.commit()

    path = sync_workspace_to_disk(workspace)

    tasks: list[Task] = list(workspace.exam.tasks)
    if task_id is not None:
        tasks = [t for t in tasks if t.id == task_id]

    results: list[TestResult] = []
    points_earned = 0.0
    points_possible = 0.0

    for task in sorted(tasks, key=lambda t: t.order_index):
        for tc in task.test_cases:
            points_possible += tc.points
            try:
                extra = json.loads(tc.input_files or "{}")
            except json.JSONDecodeError:
                extra = {}

            exec_result = execute_python(path, stdin=tc.stdin or "", extra_files=extra or None)
            actual = _normalize_output(exec_result.output)
            expected = _normalize_output(tc.expected_output)
            passed = actual == expected and exec_result.exit_code == 0

            earned = tc.points if passed else 0
            points_earned += earned

            results.append(
                TestResult(
                    test_case_id=tc.id,
                    name=tc.name,
                    passed=passed,
                    points_earned=earned,
                    points_possible=tc.points,
                    expected=None if tc.is_hidden else expected,
                    actual=None if tc.is_hidden else actual,
                    error="" if passed else (exec_result.error or ("Wrong answer" if exec_result.exit_code == 0 else f"Exit code {exec_result.exit_code}")),
                    runtime=exec_result.runtime,
                    is_hidden=tc.is_hidden,
                )
            )

    submission = Submission(
        workspace_id=workspace.id,
        task_id=task_id,
        points_earned=points_earned,
        points_possible=points_possible,
        result_json=json.dumps([r.model_dump() for r in results]),
    )
    db.add(submission)
    db.commit()

    return JudgeResponse(
        points_earned=points_earned,
        points_possible=points_possible,
        results=results,
    )
