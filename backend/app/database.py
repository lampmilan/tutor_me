from collections.abc import Generator

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import get_settings

settings = get_settings()

connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
engine = create_engine(settings.database_url, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def ensure_schema() -> None:
    """Lightweight additive migrations for create_all-managed schemas."""
    insp = inspect(engine)
    if "tasks" in insp.get_table_names():
        cols = {c["name"] for c in insp.get_columns("tasks")}
        with engine.begin() as conn:
            if "hints_json" not in cols:
                conn.execute(text("ALTER TABLE tasks ADD COLUMN hints_json TEXT DEFAULT '[]'"))
            if "solution_file" not in cols:
                conn.execute(
                    text("ALTER TABLE tasks ADD COLUMN solution_file VARCHAR(255) DEFAULT 'main.py'")
                )


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
