from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models import Exam, File, Task, Workspace
from app.schemas import ExecuteRequest, ExecuteResponse, JudgeRequest, JudgeResponse
from app.services.executor import execute_python
from app.services.judge import judge_workspace
from app.services.workspace import sync_workspace_to_disk

router = APIRouter(tags=["execution"])


def _upsert_code(db: Session, workspace: Workspace, filename: str, code: str) -> None:
    existing = next((f for f in workspace.files if f.filename == filename), None)
    if existing is None:
        created = File(
            workspace_id=workspace.id,
            filename=filename,
            content=code,
            read_only=False,
        )
        db.add(created)
        workspace.files.append(created)
    else:
        existing.content = code
    db.commit()


@router.post("/execute", response_model=ExecuteResponse)
def execute(body: ExecuteRequest, db: Session = Depends(get_db)):
    workspace = (
        db.query(Workspace)
        .options(joinedload(Workspace.files), joinedload(Workspace.exam))
        .filter(Workspace.id == body.workspace_id)
        .first()
    )
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")

    entrypoint = body.filename or "main.py"
    if body.code is not None:
        _upsert_code(db, workspace, entrypoint, body.code)

    path = sync_workspace_to_disk(workspace)
    result = execute_python(path, entrypoint=entrypoint, stdin=body.stdin or "")
    return ExecuteResponse(
        output=result.output,
        error=result.error,
        runtime=result.runtime,
        exit_code=result.exit_code,
    )


@router.post("/judge", response_model=JudgeResponse)
def judge(body: JudgeRequest, db: Session = Depends(get_db)):
    workspace = (
        db.query(Workspace)
        .options(joinedload(Workspace.files), joinedload(Workspace.exam))
        .filter(Workspace.id == body.workspace_id)
        .first()
    )
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")

    exam = (
        db.query(Exam)
        .options(joinedload(Exam.tasks).joinedload(Task.test_cases))
        .filter(Exam.id == workspace.exam_id)
        .first()
    )
    workspace.exam = exam

    return judge_workspace(
        db,
        workspace,
        task_id=body.task_id,
        code=body.code,
        filename=body.filename,
    )
