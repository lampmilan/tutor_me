"""Oracle for Locsoló — students never see this module."""

from __future__ import annotations

from collections import Counter
from typing import Any, Callable

from app.exams.builders import Row, _nonempty_lines


def parse_locsolo(content: str) -> list[Row]:
    lines = _nonempty_lines(content)
    cmd = lines[0].replace(" ", "") if lines else ""
    return [{"index": 1, "parancs": cmd, "n": len(cmd)}]


def parse(content: str) -> list[Row]:
    return parse_locsolo(content)


def _cmd(rows: list[Row]) -> str:
    return str(rows[0]["parancs"]) if rows else ""


def _simulate(cmd: str) -> tuple[int, int]:
    x = y = 0
    face = 0  # 0 N, 1 E, 2 S, 3 W
    dx = (0, 1, 0, -1)
    dy = (1, 0, -1, 0)
    for ch in cmd:
        if ch == "E":
            x += dx[face]
            y += dy[face]
        elif ch == "J":
            face = (face + 1) % 4
        elif ch == "B":
            face = (face - 1) % 4
    return x, y


def _task_locsolo_count(rows: list[Row], _spec: dict[str, Any]) -> str:
    c = Counter(_cmd(rows))
    return (
        f"E betuk szama: {c.get('E', 0)}\n"
        f"J betuk szama: {c.get('J', 0)}\n"
        f"B betuk szama: {c.get('B', 0)}"
    )


def _task_locsolo_path(rows: list[Row], _spec: dict[str, Any]) -> str:
    x, y = _simulate(_cmd(rows))
    return (
        f"A vegso helyzet: kelet {x}, eszak {y}\n"
        f"A Manhattan-tavolsag: {abs(x) + abs(y)}"
    )


def _task_locsolo_return(rows: list[Row], _spec: dict[str, Any]) -> str:
    x, y = _simulate(_cmd(rows))
    if x == 0 and y == 0:
        return "A locsolo visszater a kiindulo pontra."
    return "A locsolo nem tert vissza a kiindulo pontra."


TASK_BUILDERS: dict[str, Callable[[list[Row], dict[str, Any]], str]] = {
    "locsolo_count": _task_locsolo_count,
    "locsolo_path": _task_locsolo_path,
    "locsolo_return": _task_locsolo_return,
}
