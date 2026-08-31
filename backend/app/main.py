from contextlib import asynccontextmanager

import posthog as posthog_client
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.api import exams, execution, workspaces
from app.config import get_settings
from app.database import Base, SessionLocal, engine, ensure_schema
from app.seed import seed_all_exams
from app.services.workspace import ensure_workspaces_root

_SEED_LOCK_ID = 872341


@asynccontextmanager
async def lifespan(_: FastAPI):
    settings = get_settings()
    if settings.posthog_api_key:
        posthog_client.api_key = settings.posthog_api_key
        posthog_client.host = settings.posthog_host
        posthog_client.debug = False
    ensure_workspaces_root()
    Base.metadata.create_all(bind=engine)
    ensure_schema()
    db = SessionLocal()
    try:
        # Missing catalog folders only — do not rematerialize or TTL-sweep here.
        # Full reseed: POST /internal/seed-exams. Cleanup: POST /internal/cleanup-workspaces.
        use_lock = (
            engine.dialect.name == "postgresql"
            and "-pooler." not in settings.database_url
        )
        if use_lock:
            db.execute(text("SELECT pg_advisory_lock(:id)"), {"id": _SEED_LOCK_ID})
            db.commit()
            try:
                seed_all_exams(db, rematerialize=False)
            finally:
                db.execute(text("SELECT pg_advisory_unlock(:id)"), {"id": _SEED_LOCK_ID})
                db.commit()
        else:
            seed_all_exams(db, rematerialize=False)
    finally:
        db.close()
    yield


app = FastAPI(
    title="Érettségi Coding Practice API",
    description="Online coding practice platform for the Hungarian programming érettségi",
    version="0.1.0",
    lifespan=lifespan,
)

_settings = get_settings()
app.add_middleware(
    CORSMiddleware,
    **_settings.cors_middleware_kwargs(),
)

app.include_router(exams.router)
app.include_router(workspaces.router)
app.include_router(execution.router)


@app.get("/health")
def health():
    settings = get_settings()
    return {
        "status": "ok",
        "execution_backend": settings.execution_backend,
        "ai_generation_enabled": settings.ai_generation_enabled,
    }
