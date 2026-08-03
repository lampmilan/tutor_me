from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models import Exam, Task
from app.schemas import ExamListItem, ExamOut
from app.schemas.templates import TemplateGenerateBody
from app.services.templates import create_exam_from_template

router = APIRouter(prefix="/exams", tags=["exams"])


@router.get("", response_model=list[ExamListItem])
def list_exams(db: Session = Depends(get_db)):
    return db.query(Exam).order_by(Exam.id).all()


@router.post("/from-template", response_model=ExamOut)
def generate_from_template(
    body: TemplateGenerateBody | None = None,
    db: Session = Depends(get_db),
):
    """Create an exam from a catalog exam id or template (Phase 7)."""
    payload = body or TemplateGenerateBody()
    try:
        exam = create_exam_from_template(
            db,
            template=payload.template,
            exam_id=payload.exam_id,
            use_ai=payload.use_ai,
            seed=payload.seed,
        )
    except (FileNotFoundError, ValueError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return (
        db.query(Exam)
        .options(joinedload(Exam.files), joinedload(Exam.tasks).joinedload(Task.test_cases))
        .filter(Exam.id == exam.id)
        .first()
    )


@router.get("/{exam_id}", response_model=ExamOut)
def get_exam(exam_id: int, db: Session = Depends(get_db)):
    exam = (
        db.query(Exam)
        .options(
            joinedload(Exam.files),
            joinedload(Exam.tasks).joinedload(Task.test_cases),
        )
        .filter(Exam.id == exam_id)
        .first()
    )
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    return exam
