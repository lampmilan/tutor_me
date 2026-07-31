from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models import Exam, File, Task, Workspace
from app.schemas import ExecuteRequest, ExecuteResponse, JudgeRequest, JudgeResponse
from app.services.executor import execute_python
from app.services.judge import judge_workspace
from app.services.workspace import sync_workspace_to_disk

router = APIRouter(tags=["execution"])


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

    if body.code is not None:
        main = next((f for f in workspace.files if f.filename == "main.py"), None)
        if main is None:
            main = File(workspace_id=workspace.id, filename="main.py", content=body.code, read_only=False)
            db.add(main)
            workspace.files.append(main)
        else:
            main.content = body.code
        db.commit()

    path = sync_workspace_to_disk(workspace)
    result = execute_python(path, stdin=body.stdin or "")
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

    # Ensure tasks + test cases are loaded
    exam = (
        db.query(Exam)
        .options(joinedload(Exam.tasks).joinedload(Task.test_cases))
        .filter(Exam.id == workspace.exam_id)
        .first()
    )
    workspace.exam = exam

    return judge_workspace(db, workspace, task_id=body.task_id, code=body.code)
