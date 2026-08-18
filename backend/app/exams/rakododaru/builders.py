"""Oracle for Rakodódaru — students never see this module."""

from __future__ import annotations

from typing import Any, Callable

from app.exams.builders import Row, _nonempty_lines

START_POS = 15
MAX_POS = 30
MAX_LOAD = 5


def parse_rakododaru(content: str) -> list[Row]:
    rows: list[Row] = []
    for i, line in enumerate(_nonempty_lines(content), start=1):
        parts = line.split()
        rows.append({"index": i, "op": parts[0], "arg": int(parts[1])})
    return rows


def parse(content: str) -> list[Row]:
    return parse_rakododaru(content)


def _reason(pos: int, load: int) -> str | None:
    if pos < 1 or pos > MAX_POS:
        return "palyan kivul"
    if load < 0:
        return "negativ teher"
    if load > MAX_LOAD:
        return "tulterheles"
    return None


def _run(rows: list[Row]) -> tuple[int, int, list[tuple[int, int, int]], tuple[int, str] | None]:
    pos = START_POS
    load = 0
    log: list[tuple[int, int, int]] = []
    first: tuple[int, str] | None = None
    for row in rows:
        op, n = str(row["op"]), int(row["arg"])
        if op == "J":
            pos += n
        elif op == "B":
            pos -= n
        elif op == "FEL":
            load += n
        elif op == "LE":
            load -= n
        why = _reason(pos, load)
        if why is not None and first is None:
            first = (int(row["index"]), why)
        log.append((int(row["index"]), pos, load))
    return pos, load, log, first


def _task_rakododaru_count(rows: list[Row], _spec: dict[str, Any]) -> str:
    return f"A parancsok szama: {len(rows)}"


def _task_rakododaru_veg(rows: list[Row], _spec: dict[str, Any]) -> str:
    pos, load, _log, _first = _run(rows)
    return f"A vegso allas: {pos}\nA vegso teher: {load}"


def _task_rakododaru_szabaly(rows: list[Row], _spec: dict[str, Any]) -> str:
    _pos, _load, _log, first = _run(rows)
    if first is None:
        return "A daru vegig szabalyos maradt."
    return "A daru legalabb egyszer szabalyt szegett."


def _task_rakododaru_elso_hiba(rows: list[Row], _spec: dict[str, Any]) -> str:
    _pos, _load, _log, first = _run(rows)
    if first is None:
        return ""
    return f"Az elso hibas parancs: {first[0]}, ok: {first[1]}"


def _task_rakododaru_file(rows: list[Row], _spec: dict[str, Any]) -> str:
    _pos, _load, log, _first = _run(rows)
    return "\n".join(f"{i} {p} {t}" for i, p, t in log)


TASK_BUILDERS: dict[str, Callable[[list[Row], dict[str, Any]], str]] = {
    "rakododaru_count": _task_rakododaru_count,
    "rakododaru_veg": _task_rakododaru_veg,
    "rakododaru_szabaly": _task_rakododaru_szabaly,
    "rakododaru_elso_hiba": _task_rakododaru_elso_hiba,
    "rakododaru_file": _task_rakododaru_file,
}
