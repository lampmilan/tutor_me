from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import exams, execution, workspaces
from app.config import get_settings
from app.database import Base, SessionLocal, engine
from app.db.migrate import ensure_schema
from app.seed import seed_cities_exam
from app.services.workspace import ensure_workspaces_root


@asynccontextmanager
async def lifespan(_: FastAPI):
    settings = get_settings()
    ensure_workspaces_root()
    Base.metadata.create_all(bind=engine)
    ensure_schema(engine)
    db = SessionLocal()
    try:
        seed_cities_exam(db)
    finally:
        db.close()
    yield


app = FastAPI(
    title="Érettségi Coding Practice API",
    description="Online coding practice platform for the Hungarian programming érettségi",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
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
