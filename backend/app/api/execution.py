from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models import Exam, File, Task, Workspace
from app.schemas import ExecuteRequest, ExecuteResponse, JudgeRequest, JudgeResponse
from app.services.executor import execute_python
from app.services.judge import RUN_ENTRYPOINT, judge_workspace, prepare_run, student_code_for_task
from app.services.rate_limit import limit_execute, limit_judge
from app.services.workspace import sync_workspace_to_disk, touch_workspace

router = APIRouter(tags=["execution"])


@router.post("/execute", response_model=ExecuteResponse, dependencies=[Depends(limit_execute)])
def execute(body: ExecuteRequest, request: Request, db: Session = Depends(get_db)):
    visitor_id: str | None = request.headers.get("x-visitor-id")
    workspace = (
        db.query(Workspace)
        .options(
            joinedload(Workspace.files),
            joinedload(Workspace.exam).joinedload(Exam.tasks),
        )
        .filter(Workspace.id == body.workspace_id)
        .first()
    )
    if not workspace:
        raise HTTPException(status_code=404, detail="A munkaterület nem található.")
    touch_workspace(db, workspace)

    try:
        task: Task | None = None
        if body.task_id is not None:
            task = next((t for t in workspace.exam.tasks if t.id == body.task_id), None)
            if task is None:
                raise HTTPException(status_code=404, detail="A feladat nem található.")
        elif body.filename:
            task = next(
                (t for t in workspace.exam.tasks if t.solution_file == body.filename),
                None,
            )
        if task is None:
            tasks = sorted(workspace.exam.tasks, key=lambda t: t.order_index)
            task = tasks[0] if tasks else None

        if task is None:
            if body.code is not None:
                main = next((f for f in workspace.files if f.filename == RUN_ENTRYPOINT), None)
                if main is None:
                    main = File(
                        workspace_id=workspace.id,
                        filename=RUN_ENTRYPOINT,
                        content=body.code,
                        read_only=False,
                    )
                    db.add(main)
                    workspace.files.append(main)
                else:
                    main.content = body.code
                db.commit()
            path = sync_workspace_to_disk(workspace)
            result = execute_python(
                path,
                entrypoint=RUN_ENTRYPOINT,
                stdin=body.stdin or "",
                visitor_id=visitor_id,
                exam_id=workspace.exam_id,
                task_id=None,
                workspace_id=workspace.id,
            )
        else:
            student_code = (
                body.code if body.code is not None else student_code_for_task(workspace, task, None)
            )
            path = prepare_run(db, workspace, task, student_code)
            stdin = body.stdin if body.stdin else (task.stdin or "")
            capture = [task.expected_file] if (task.expected_file or "").strip() else None
            result = execute_python(
                path,
                entrypoint=RUN_ENTRYPOINT,
                stdin=stdin,
                capture_files=capture,
                isolate=bool(capture),
                visitor_id=visitor_id,
                exam_id=workspace.exam_id,
                task_id=task.id,
                workspace_id=workspace.id,
            )

        output = result.output
        if result.files:
            chunks = [output.rstrip()] if output.strip() else []
            for name, content in result.files.items():
                chunks.append(f"--- {name} ---\n{content.rstrip()}")
            output = "\n\n".join(chunks) + ("\n" if chunks else "")

        return ExecuteResponse(
            output=output,
            error=result.error,
            runtime=result.runtime,
            exit_code=result.exit_code,
        )
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Futtatás sikertelen: {exc}") from exc


@router.post("/judge", response_model=JudgeResponse, dependencies=[Depends(limit_judge)])
def judge(body: JudgeRequest, db: Session = Depends(get_db)):
    workspace = (
        db.query(Workspace)
        .options(joinedload(Workspace.files), joinedload(Workspace.exam))
        .filter(Workspace.id == body.workspace_id)
        .first()
    )
    if not workspace:
        raise HTTPException(status_code=404, detail="A munkaterület nem található.")
    touch_workspace(db, workspace)

    exam = (
        db.query(Exam)
        .options(joinedload(Exam.tasks).joinedload(Task.test_cases))
        .filter(Exam.id == workspace.exam_id)
        .first()
    )
    workspace.exam = exam

    try:
        return judge_workspace(
            db,
            workspace,
            task_id=body.task_id,
            code=body.code,
            filename=body.filename,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Értékelés sikertelen: {exc}") from exc
