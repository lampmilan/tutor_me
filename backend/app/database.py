from collections.abc import Generator

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from sqlalchemy.pool import NullPool

from app.config import get_settings

settings = get_settings()


def sqlalchemy_database_url(url: str) -> str:
    """Normalize Neon / libpq URLs for SQLAlchemy + psycopg2."""
    if url.startswith("postgres://"):
        url = "postgresql://" + url[len("postgres://") :]
    if url.startswith("postgresql://") and "+psycopg2" not in url and "+asyncpg" not in url:
        url = "postgresql+psycopg2://" + url[len("postgresql://") :]
    return url


def _make_engine(url: str) -> Engine:
    sa_url = sqlalchemy_database_url(url)
    is_sqlite = sa_url.startswith("sqlite")
    connect_args: dict = {}
    if is_sqlite:
        connect_args["check_same_thread"] = False
        return create_engine(sa_url, connect_args=connect_args)

    # Neon pooled endpoints sit behind PgBouncer (transaction pooling).
    # Disable SQLAlchemy's pool so we don't double-pool.
    is_neon_pooler = "-pooler." in sa_url
    kwargs: dict = {"pool_pre_ping": True}
    if is_neon_pooler:
        kwargs["poolclass"] = NullPool
    else:
        kwargs["pool_size"] = 5
        kwargs["max_overflow"] = 5
        kwargs["pool_recycle"] = 280
    if "sslmode=" not in sa_url and "neon.tech" in sa_url:
        connect_args["sslmode"] = "require"
    return create_engine(sa_url, connect_args=connect_args, **kwargs)


engine = _make_engine(settings.database_url)
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
    _add_column_if_missing("tasks", "solution_file", "solution_file VARCHAR(255) DEFAULT 'main.py'")
    _add_column_if_missing("tasks", "uses_preamble", "uses_preamble BOOLEAN DEFAULT FALSE")
    _add_column_if_missing("tasks", "starter", "starter TEXT DEFAULT ''")
    _add_column_if_missing("exams", "preamble", "preamble TEXT DEFAULT ''")
    _add_column_if_missing("exams", "shared_variable", "shared_variable VARCHAR(100) DEFAULT 'data'")
    _add_column_if_missing("exams", "level", "level VARCHAR(20) DEFAULT 'kozep'")
    _add_column_if_missing("exams", "origin", "origin VARCHAR(20) DEFAULT 'synthetic'")
    _add_column_if_missing("exams", "difficulty", "difficulty INTEGER DEFAULT 2")
    _add_column_if_missing("exams", "tags_json", "tags_json TEXT DEFAULT '[]'")
    _add_column_if_missing("exams", "constraints_json", "constraints_json TEXT DEFAULT '[]'")
    _add_column_if_missing("exams", "data_explanation", "data_explanation TEXT DEFAULT ''")
    _add_column_if_missing("tasks", "tags_json", "tags_json TEXT DEFAULT '[]'")
    _add_column_if_missing("tasks", "stdin", "stdin TEXT DEFAULT ''")
    _add_column_if_missing("tasks", "expected_file", "expected_file VARCHAR(255) DEFAULT ''")
    _add_column_if_missing("workspaces", "last_accessed_at", "last_accessed_at TIMESTAMP")
    _add_column_if_missing("feedback", "rating", "rating INTEGER")
    _add_column_if_missing(
        "feedback", "would_pay_for_json", "would_pay_for_json TEXT DEFAULT '[]'"
    )


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
