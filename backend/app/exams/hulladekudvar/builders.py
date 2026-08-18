"""Oracle for Hulladékudvar — students never see this module."""

from __future__ import annotations

from typing import Any, Callable

from app.exams.builders import Row, _nonempty_lines

EGYSEG = {"PAPIR": 5, "UV": 15, "FEM": 20, "ZOLD": 2, "UREG": 8}


def parse_hulladekudvar(content: str) -> list[Row]:
    rows: list[Row] = []
    for i, line in enumerate(_nonempty_lines(content), start=1):
        parts = line.split()
        kod, kg = parts[0], int(parts[1])
        rows.append(
            {
                "index": i,
                "kod": kod,
                "kg": kg,
                "pont": EGYSEG.get(kod, 0) * kg,
            }
        )
    return rows


def parse(content: str) -> list[Row]:
    return parse_hulladekudvar(content)


def _task_hulladekudvar_count(rows: list[Row], _spec: dict[str, Any]) -> str:
    return f"A tetelsorok szama: {len(rows)}\nAz ossztomeg: {sum(int(r['kg']) for r in rows)} kg"


def _task_hulladekudvar_pont(rows: list[Row], _spec: dict[str, Any]) -> str:
    return f"A kiosztott pontok: {sum(int(r['pont']) for r in rows)}"


def _task_hulladekudvar_tipus(rows: list[Row], spec: dict[str, Any]) -> str:
    kod = str(spec.get("stdin") or "").strip().split()[0]
    lines = ["Adja meg az anyag kodjat!"]
    hits = [r for r in rows if r["kod"] == kod]
    if not hits:
        lines.append("Nincs ilyen tipus.")
        return "\n".join(lines)
    lines.append(f"A tipus tomege: {sum(int(r['kg']) for r in hits)} kg")
    lines.append(f"A tipus pontjai: {sum(int(r['pont']) for r in hits)}")
    return "\n".join(lines)


TASK_BUILDERS: dict[str, Callable[[list[Row], dict[str, Any]], str]] = {
    "hulladekudvar_count": _task_hulladekudvar_count,
    "hulladekudvar_pont": _task_hulladekudvar_pont,
    "hulladekudvar_tipus": _task_hulladekudvar_tipus,
}
