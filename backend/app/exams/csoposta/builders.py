"""Oracle for Csőposta — students never see this module."""

from __future__ import annotations

from typing import Any, Callable

from app.exams.builders import Row, _nonempty_lines

STATIONS = 16
TRANSFER = {4, 9, 13}
EXTRA = 2


def parse_csoposta(content: str) -> list[Row]:
    rows: list[Row] = []
    index = 0
    for line in _nonempty_lines(content):
        for token in line.replace(",", " ").split():
            index += 1
            rows.append({"index": index, "lepes": int(token)})
    return rows


def parse(content: str) -> list[Row]:
    return parse_csoposta(content)


def _walk(rows: list[Row]) -> tuple[int, int]:
    pos = 1
    hits = 0
    for row in rows:
        pos = (pos - 1 + int(row["lepes"])) % STATIONS + 1
        if pos in TRANSFER:
            hits += 1
            pos = (pos - 1 + EXTRA) % STATIONS + 1
    return pos, hits


def _task_csoposta_count(rows: list[Row], _spec: dict[str, Any]) -> str:
    return f"A lepesek szama: {len(rows)}"


def _task_csoposta_veg(rows: list[Row], _spec: dict[str, Any]) -> str:
    pos, _hits = _walk(rows)
    return f"A kapszula vegallomasa: {pos}"


def _task_csoposta_atrako(rows: list[Row], _spec: dict[str, Any]) -> str:
    _pos, hits = _walk(rows)
    return f"Az atrako erintesek szama: {hits}"


TASK_BUILDERS: dict[str, Callable[[list[Row], dict[str, Any]], str]] = {
    "csoposta_count": _task_csoposta_count,
    "csoposta_veg": _task_csoposta_veg,
    "csoposta_atrako": _task_csoposta_atrako,
}
