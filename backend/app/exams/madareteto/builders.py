"""Oracle for Madáretető — students never see this module."""

from __future__ import annotations

from typing import Any, Callable

from app.exams.builders import Row, _nonempty_lines


def parse_madareteto(content: str) -> list[Row]:
    rows: list[Row] = []
    index = 0
    for line in _nonempty_lines(content):
        for token in line.replace(",", " ").split():
            index += 1
            rows.append({"index": index, "gramm": int(token)})
    return rows


def parse(content: str) -> list[Row]:
    return parse_madareteto(content)


def _task_madareteto_sum(rows: list[Row], _spec: dict[str, Any]) -> str:
    return f"A heti eleseg: {sum(int(r['gramm']) for r in rows)} g"


def _task_madareteto_max(rows: list[Row], _spec: dict[str, Any]) -> str:
    peak = max(int(r["gramm"]) for r in rows)
    best = min((r for r in rows if int(r["gramm"]) == peak), key=lambda r: r["index"])
    return f"A legnagyobb adag: {best['gramm']} g, {best['index']}. nap."


def _task_madareteto_jutalom(rows: list[Row], _spec: dict[str, Any]) -> str:
    grams = [int(r["gramm"]) for r in rows]
    for i in range(len(grams) - 2):
        if grams[i] >= 50 and grams[i + 1] >= 50 and grams[i + 2] >= 50:
            return "Jutalom jar."
    return "Nincs jutalom."


TASK_BUILDERS: dict[str, Callable[[list[Row], dict[str, Any]], str]] = {
    "madareteto_sum": _task_madareteto_sum,
    "madareteto_max": _task_madareteto_max,
    "madareteto_jutalom": _task_madareteto_jutalom,
}
