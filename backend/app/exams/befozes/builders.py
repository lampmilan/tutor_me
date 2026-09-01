"""Oracle for Fogások — students never see this module.

Student runtime gets the file as a raw string via the preamble.
"""

from __future__ import annotations

from typing import Any, Callable

from app.exams.builders import Row, _nonempty_lines


def parse_fogasok(content: str) -> list[Row]:
    rows: list[Row] = []
    index = 0
    for line in _nonempty_lines(content):
        for token in line.replace(",", " ").split():
            index += 1
            rows.append({"index": index, "tomeg": int(token)})
    return rows


def parse(content: str) -> list[Row]:
    return parse_fogasok(content)


def _task_fogasok_count(rows: list[Row], _spec: dict[str, Any]) -> str:
    return f"A fogasok szama: {len(rows)}"


def _task_fogasok_max(rows: list[Row], _spec: dict[str, Any]) -> str:
    peak = max(r["tomeg"] for r in rows)
    best = min((r for r in rows if r["tomeg"] == peak), key=lambda r: r["index"])
    return f"A legnagyobb hal: {best['tomeg']} dkg, {best['index']}. a sorban."


def _task_fogasok_threshold(rows: list[Row], spec: dict[str, Any]) -> str:
    raw = str(spec.get("stdin") or "0").strip().split()[0]
    limit = int(raw)
    n = sum(1 for r in rows if int(r["tomeg"]) >= limit)
    return (
        "Kategoria also hatara (dkg):\n"
        f"Legalabb {limit} dkg-os halak szama: {n}"
    )


TASK_BUILDERS: dict[str, Callable[[list[Row], dict[str, Any]], str]] = {
    "fogasok_count": _task_fogasok_count,
    "fogasok_max": _task_fogasok_max,
    "fogasok_threshold": _task_fogasok_threshold,
}
