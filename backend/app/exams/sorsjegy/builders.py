"""Oracle for Sorsjegy — students never see this module."""

from __future__ import annotations

import random
from typing import Any, Callable

from app.exams.builders import Row

SEED = 2027


def parse_sorsjegy(_content: str) -> list[Row]:
    random.seed(SEED)
    nums = random.sample(range(1, 51), 8)
    return [{"index": i, "szam": n, "nums": nums} for i, n in enumerate(nums, start=1)]


def parse(content: str) -> list[Row]:
    return parse_sorsjegy(content)


def _nums(rows: list[Row]) -> list[int]:
    if rows and "nums" in rows[0]:
        return list(rows[0]["nums"])
    return [int(r["szam"]) for r in rows]


def _task_sorsjegy_szamok(rows: list[Row], _spec: dict[str, Any]) -> str:
    return "A nyero szamok: " + " ".join(str(n) for n in _nums(rows))


def _task_sorsjegy_minmax(rows: list[Row], _spec: dict[str, Any]) -> str:
    nums = _nums(rows)
    return (
        f"A legkisebb nyero szam: {min(nums)}\n"
        f"A legnagyobb nyero szam: {max(nums)}"
    )


def _task_sorsjegy_sajat(rows: list[Row], spec: dict[str, Any]) -> str:
    raw = str(spec.get("stdin") or "0").strip().split()[0]
    sajat = int(raw)
    hit = sajat in _nums(rows)
    msg = "Nyert!" if hit else "Nem nyert."
    return f"A sajat szelveny szama:\n{msg}"


TASK_BUILDERS: dict[str, Callable[[list[Row], dict[str, Any]], str]] = {
    "sorsjegy_szamok": _task_sorsjegy_szamok,
    "sorsjegy_minmax": _task_sorsjegy_minmax,
    "sorsjegy_sajat": _task_sorsjegy_sajat,
}
