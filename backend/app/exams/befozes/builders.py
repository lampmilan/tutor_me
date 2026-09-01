"""Oracle for Befőzés — students never see this module.

Student runtime gets the file as a raw string via the preamble.
"""

from __future__ import annotations

from typing import Any, Callable

from app.exams.builders import Row, _nonempty_lines

PROMPT = "Mari néni lekvárja (dl):"


def parse_befozes(content: str) -> list[Row]:
    rows: list[Row] = []
    index = 0
    for line in _nonempty_lines(content):
        for token in line.replace(",", " ").split():
            index += 1
            rows.append({"index": index, "meret": int(token)})
    n = len(rows)
    for row in rows:
        row["n"] = n
    if not rows:
        rows.append({"index": 0, "meret": 0, "n": 0, "_empty": True})
    return rows


def parse(content: str) -> list[Row]:
    return parse_befozes(content)


def _jars(rows: list[Row]) -> list[Row]:
    return [r for r in rows if r.get("index") and not r.get("_empty")]


def _lekvar_dl(spec: dict[str, Any]) -> int:
    raw = str(spec.get("stdin") or "0").strip().split()[0]
    return int(raw)


def _task_befozes_beker(_rows: list[Row], _spec: dict[str, Any]) -> str:
    return PROMPT


def _task_befozes_max(rows: list[Row], _spec: dict[str, Any]) -> str:
    jars = _jars(rows)
    peak = max(int(r["meret"]) for r in jars)
    best = min((r for r in jars if int(r["meret"]) == peak), key=lambda r: int(r["index"]))
    return f"A legnagyobb üveg: {best['meret']} dl és {best['index']}. a sorban."


def _task_befozes_elegendo(rows: list[Row], spec: dict[str, Any]) -> str:
    lekvar = _lekvar_dl(spec)
    total = sum(int(r["meret"]) for r in _jars(rows))
    msg = "Elegendő üveg volt." if total >= lekvar else "Maradt lekvár."
    return f"{PROMPT}\n{msg}"


TASK_BUILDERS: dict[str, Callable[[list[Row], dict[str, Any]], str]] = {
    "befozes_beker": _task_befozes_beker,
    "befozes_max": _task_befozes_max,
    "befozes_elegendo": _task_befozes_elegendo,
}
