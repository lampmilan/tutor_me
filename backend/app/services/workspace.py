from datetime import datetime, timedelta, timezone
from pathlib import Path
import shutil

from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from app.config import get_settings
from app.models import Exam, ExamFile, File, Submission, Workspace


def ensure_workspaces_root() -> Path:
    root = Path(get_settings().workspaces_root)
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


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def touch_workspace(db: Session, workspace: Workspace) -> None:
    """Record activity so TTL cleanup keeps live student work."""
    workspace.last_accessed_at = _utcnow()
    db.add(workspace)
    db.commit()


def create_workspace(db: Session, exam: Exam, user_id: str = "anonymous") -> Workspace:
    """Create a workspace for an exam and copy template files onto disk."""
    now = _utcnow()
    workspace = Workspace(
        exam_id=exam.id,
        user_id=user_id,
        path="",
        last_accessed_at=now,
    )
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
        touch_workspace(db, workspace)
    return file


def delete_workspace(db: Session, workspace: Workspace) -> None:
    """Remove DB rows (files + submissions) and the on-disk sandbox if present."""
    path = Path(workspace.path) if workspace.path else None
    db.query(Submission).filter(Submission.workspace_id == workspace.id).delete(
        synchronize_session=False
    )
    db.delete(workspace)
    db.flush()
    if path is not None and path.exists():
        shutil.rmtree(path, ignore_errors=True)


def cleanup_expired_workspaces(db: Session, ttl_days: int | None = None) -> int:
    """Delete workspaces idle longer than TTL. ttl_days <= 0 disables cleanup."""
    days = get_settings().workspace_ttl_days if ttl_days is None else ttl_days
    if days <= 0:
        return 0
    cutoff = _utcnow() - timedelta(days=days)
    expired = (
        db.query(Workspace)
        .filter(
            or_(
                Workspace.last_accessed_at < cutoff,
                and_(Workspace.last_accessed_at.is_(None), Workspace.created_at < cutoff),
            )
        )
        .all()
    )
    count = 0
    for workspace in expired:
        delete_workspace(db, workspace)
        count += 1
    if count:
        db.commit()
    return count
