"""User-initiated feedback. Stored even when analytics cookies are declined."""

from __future__ import annotations

import json
import logging
import uuid
from datetime import datetime, timezone

import posthog as posthog_client
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.api.ops_auth import require_ops_token
from app.config import get_settings
from app.database import get_db
from app.models import Feedback
from app.schemas import FeedbackCreated, FeedbackIn, FeedbackOut
from app.services.rate_limit import limit_feedback

router = APIRouter(tags=["feedback"])
_log = logging.getLogger("feedback")


@router.post("/feedback", response_model=FeedbackCreated, dependencies=[Depends(limit_feedback)])
def submit_feedback(body: FeedbackIn, request: Request, db: Session = Depends(get_db)):
    row = Feedback(
        feedback_type=body.feedback_type,
        exam_title=body.exam_title or "",
        task_title=body.task_title or "",
        message=body.message or "",
        rating=body.rating,
        would_pay_for_json=json.dumps(body.would_pay_for or []),
        created_at=datetime.now(timezone.utc),
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    _capture_posthog(row, visitor_id=request.headers.get("x-visitor-id"))
    return FeedbackCreated(id=row.id)


@router.get("/internal/feedback", response_model=list[FeedbackOut])
def list_feedback(request: Request, db: Session = Depends(get_db), limit: int = 100):
    require_ops_token(request)
    cap = min(max(limit, 1), 500)
    return (
        db.query(Feedback)
        .order_by(Feedback.created_at.desc(), Feedback.id.desc())
        .limit(cap)
        .all()
    )


def _capture_posthog(row: Feedback, visitor_id: str | None) -> None:
    settings = get_settings()
    if not settings.posthog_api_key:
        return
    distinct = (visitor_id or "").strip() or f"feedback:{uuid.uuid4()}"
    properties: dict = {
        "feedback_type": row.feedback_type,
        "exam_title": row.exam_title or None,
        "task_title": row.task_title or None,
        "message": row.message or None,
        "$process_person_profile": False,
    }
    if row.feedback_type == "problem":
        properties["problem"] = row.message
    elif row.feedback_type == "product":
        properties["rating"] = row.rating
        properties["would_pay_for"] = row.would_pay_for
        if row.message:
            properties["feedback"] = row.message
    else:
        properties["feedback"] = row.message
    try:
        posthog_client.capture(
            distinct_id=distinct,
            event="feedback_submitted",
            properties=properties,
        )
    except Exception:
        _log.warning("PostHog capture failed for feedback id=%s", row.id, exc_info=True)
