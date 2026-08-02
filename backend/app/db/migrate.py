"""Lightweight schema patches for environments without Alembic."""

from __future__ import annotations

from sqlalchemy import inspect, text
from sqlalchemy.engine import Engine


def ensure_schema(engine: Engine) -> None:
    """Add columns introduced after initial create_all."""
    inspector = inspect(engine)
    if "tasks" not in inspector.get_table_names():
        return

    columns = {col["name"] for col in inspector.get_columns("tasks")}
    if "solution_file" not in columns:
        with engine.begin() as conn:
            conn.execute(
                text("ALTER TABLE tasks ADD COLUMN solution_file VARCHAR(255) DEFAULT 'main.py'")
            )
