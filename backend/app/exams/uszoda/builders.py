"""Oracle for Uszoda — students never see this module."""

from __future__ import annotations

from typing import Any, Callable

from app.exams.builders import Row, _nonempty_lines

ARAK = {"NAPI": 2500, "BERLET": 1800, "GYEREK": 1200}
TIE_ORDER = ("NAPI", "BERLET", "GYEREK")


def parse_uszoda(content: str) -> list[Row]:
    rows: list[Row] = []
    for i, line in enumerate(_nonempty_lines(content), start=1):
        parts = line.split()
        rows.append({"index": i, "tipus": parts[0], "db": int(parts[1])})
    return rows


def parse(content: str) -> list[Row]:
    return parse_uszoda(content)


def _totals(rows: list[Row]) -> dict[str, int]:
    tot = {k: 0 for k in ARAK}
    for row in rows:
        tot[str(row["tipus"])] = tot.get(str(row["tipus"]), 0) + int(row["db"])
    return tot


def _task_uszoda_count(rows: list[Row], _spec: dict[str, Any]) -> str:
    jegyek = sum(int(r["db"]) for r in rows)
    return f"A tetelsorok szama: {len(rows)}\nAz eladott jegyek szama: {jegyek}"


def _task_uszoda_nepszeru(rows: list[Row], _spec: dict[str, Any]) -> str:
    tot = _totals(rows)
    peak = max(tot[t] for t in TIE_ORDER)
    winner = next(t for t in TIE_ORDER if tot[t] == peak)
    return f"A legnepszerubb jegy: {winner}"


def _task_uszoda_bevetel(rows: list[Row], spec: dict[str, Any]) -> str:
    tipus = str(spec.get("stdin") or "").strip().split()[0]
    tot = _totals(rows)
    bevetel = tot.get(tipus, 0) * ARAK.get(tipus, 0)
    return f"Adja meg a jegy tipust!\nA tipus bevetel: {bevetel} Ft"


TASK_BUILDERS: dict[str, Callable[[list[Row], dict[str, Any]], str]] = {
    "uszoda_count": _task_uszoda_count,
    "uszoda_nepszeru": _task_uszoda_nepszeru,
    "uszoda_bevetel": _task_uszoda_bevetel,
}
