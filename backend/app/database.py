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


def _add_column_if_missing(table: str, column: str, ddl: str) -> None:
    insp = inspect(engine)
    if table not in insp.get_table_names():
        return
    cols = {c["name"] for c in insp.get_columns(table)}
    if column not in cols:
        with engine.begin() as conn:
            conn.execute(text(f"ALTER TABLE {table} ADD COLUMN {ddl}"))


def ensure_schema() -> None:
    """Lightweight additive migrations for create_all-managed schemas."""
    _add_column_if_missing("tasks", "hints_json", "hints_json TEXT DEFAULT '[]'")
    _add_column_if_missing("tasks", "uses_preamble", "uses_preamble BOOLEAN DEFAULT FALSE")
    _add_column_if_missing("tasks", "starter", "starter TEXT DEFAULT ''")
    _add_column_if_missing("tasks", "entry_filename", "entry_filename VARCHAR(255) DEFAULT 'main.py'")
    _add_column_if_missing("exams", "preamble", "preamble TEXT DEFAULT ''")
    _add_column_if_missing("exams", "shared_variable", "shared_variable VARCHAR(100) DEFAULT 'data'")


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
