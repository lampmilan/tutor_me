from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models import Exam, File, Workspace
from app.schemas import FileOut, FileUpdate, StartExamRequest, WorkspaceOut
from app.services.workspace import create_workspace, sync_workspace_to_disk

router = APIRouter(tags=["workspaces"])


@router.post("/exams/{exam_id}/start", response_model=WorkspaceOut)
def start_exam(exam_id: int, body: StartExamRequest | None = None, db: Session = Depends(get_db)):
    exam = (
        db.query(Exam)
        .options(joinedload(Exam.files), joinedload(Exam.tasks))
        .filter(Exam.id == exam_id)
        .first()
    )
    if not exam:
        raise HTTPException(status_code=404, detail="A feladatsor nem található.")

    user_id = (body.user_id if body else "anonymous") or "anonymous"
    workspace = create_workspace(db, exam, user_id=user_id)
    return (
        db.query(Workspace)
        .options(joinedload(Workspace.files))
        .filter(Workspace.id == workspace.id)
        .first()
    )


@router.get("/workspaces/{workspace_id}", response_model=WorkspaceOut)
def get_workspace(workspace_id: int, db: Session = Depends(get_db)):
    workspace = (
        db.query(Workspace)
        .options(joinedload(Workspace.files))
        .filter(Workspace.id == workspace_id)
        .first()
    )
    if not workspace:
        raise HTTPException(status_code=404, detail="A munkaterület nem található.")
    return workspace


@router.get("/workspaces/{workspace_id}/files/{filename}", response_model=FileOut)
def get_file(workspace_id: int, filename: str, db: Session = Depends(get_db)):
    file = (
        db.query(File)
        .filter(File.workspace_id == workspace_id, File.filename == filename)
        .first()
    )
    if not file:
        raise HTTPException(status_code=404, detail="A fájl nem található.")
    return file


@router.put("/workspaces/{workspace_id}/files/{filename}", response_model=FileOut)
def save_file(
    workspace_id: int,
    filename: str,
    body: FileUpdate,
    db: Session = Depends(get_db),
):
    workspace = (
        db.query(Workspace)
        .options(joinedload(Workspace.files))
        .filter(Workspace.id == workspace_id)
        .first()
    )
    if not workspace:
        raise HTTPException(status_code=404, detail="A munkaterület nem található.")

    file = next((f for f in workspace.files if f.filename == filename), None)
    if not file:
        raise HTTPException(status_code=404, detail="A fájl nem található.")
    if file.read_only:
        raise HTTPException(status_code=403, detail="A fájl csak olvasható.")

    file.content = body.content
    db.commit()
    sync_workspace_to_disk(workspace)
    db.refresh(file)
    return file
