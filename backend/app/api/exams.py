from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.exams.loader import unlisted_catalog_ids
from app.models import Exam, Task
from app.schemas import ExamListItem, ExamOut
from app.schemas.templates import TemplateGenerateBody
from app.services.templates import create_exam_from_template

router = APIRouter(prefix="/exams", tags=["exams"])

# Catalog is static between deploys/seeds — safe to cache at CDN/browser.
_CATALOG_CACHE = "public, max-age=60, s-maxage=300, stale-while-revalidate=600"


@router.get("", response_model=list[ExamListItem])
def list_exams(response: Response, db: Session = Depends(get_db)):
    response.headers["Cache-Control"] = _CATALOG_CACHE
    hidden = unlisted_catalog_ids()
    exams = db.query(Exam).order_by(Exam.id).all()
    return [exam for exam in exams if (exam.template_type or "") not in hidden]


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
def get_exam(exam_id: int, response: Response, db: Session = Depends(get_db)):
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
    response.headers["Cache-Control"] = _CATALOG_CACHE
    return exam
