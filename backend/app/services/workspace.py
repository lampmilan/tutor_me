from pathlib import Path

from sqlalchemy.orm import Session

from app.config import get_settings
from app.models import Exam, ExamFile, File, Workspace

settings = get_settings()


def ensure_workspaces_root() -> Path:
    root = Path(settings.workspaces_root)
    root.mkdir(parents=True, exist_ok=True)
    return root


def sync_workspace_to_disk(workspace: Workspace) -> Path:
    """Write all workspace files to the host path used by the executor."""
    root = ensure_workspaces_root()
    path = root / str(workspace.id)
    path.mkdir(parents=True, exist_ok=True)
    for f in workspace.files:
        (path / f.filename).write_text(f.content, encoding="utf-8")
    return path


def create_workspace(db: Session, exam: Exam, user_id: str = "anonymous") -> Workspace:
    """Create a workspace for an exam and copy template files onto disk."""
    workspace = Workspace(exam_id=exam.id, user_id=user_id, path="")
    db.add(workspace)
    db.flush()  # assign id

    path = ensure_workspaces_root() / str(workspace.id)
    path.mkdir(parents=True, exist_ok=True)
    workspace.path = str(path)

    files_to_copy: list[ExamFile] = list(exam.files)
    has_python = any(f.filename.endswith(".py") for f in files_to_copy)
    if not has_python:
        # Fallback editable starter when an exam has no solution files yet
        files_to_copy.append(
            ExamFile(exam_id=exam.id, filename="main.py", content="", read_only=False)
        )

    for ef in files_to_copy:
        content = ef.content
        wf = File(
            workspace_id=workspace.id,
            filename=ef.filename,
            content=content,
            read_only=ef.read_only,
        )
        db.add(wf)
        (path / ef.filename).write_text(content, encoding="utf-8")

    db.commit()
    db.refresh(workspace)
    return workspace


def get_workspace_file(workspace: Workspace, filename: str) -> File | None:
    for f in workspace.files:
        if f.filename == filename:
            return f
    return None


def update_file_content(db: Session, file: File, content: str) -> File:
    if file.read_only:
        raise ValueError(f"File {file.filename} is read-only")
    file.content = content
    db.commit()
    db.refresh(file)
    # Sync to disk
    workspace = file.workspace
    if workspace:
        sync_workspace_to_disk(workspace)
    return file
