from contextlib import asynccontextmanager

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
    ensure_workspaces_root()
    Base.metadata.create_all(bind=engine)
    ensure_schema()
    db = SessionLocal()
    try:
        use_lock = (
            engine.dialect.name == "postgresql"
            and "-pooler." not in settings.database_url
        )
        if use_lock:
            db.execute(text("SELECT pg_advisory_lock(:id)"), {"id": _SEED_LOCK_ID})
            db.commit()
            try:
                seed_all_exams(db)
            finally:
                db.execute(text("SELECT pg_advisory_unlock(:id)"), {"id": _SEED_LOCK_ID})
                db.commit()
        else:
            seed_all_exams(db)
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
_origins = _settings.cors_origin_list()
app.add_middleware(
    CORSMiddleware,
    allow_origins=_origins,
    allow_origin_regex=r"https://.*\.vercel\.app" if _origins == ["*"] else None,
    # Wildcard + credentials is rejected by browsers; Vercel same-origin rewrites
    # don't need cookies.
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
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
    }
