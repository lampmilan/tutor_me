"""Oracle for Zsilip — students never see this module."""

from __future__ import annotations

from typing import Any, Callable

from app.exams.builders import Row, _nonempty_lines


def kulonbseg(a: int, b: int) -> int:
    return abs(int(a) - int(b))


def parse_zsilip(content: str) -> list[Row]:
    rows: list[Row] = []
    for i, line in enumerate(_nonempty_lines(content), start=1):
        parts = line.split()
        rows.append(
            {
                "index": i,
                "ora": int(parts[0]),
                "perc": int(parts[1]),
                "szint": int(parts[2]),
            }
        )
    return rows


def parse(content: str) -> list[Row]:
    return parse_zsilip(content)


def _jumps(rows: list[Row]) -> list[tuple[int, int, int]]:
    out: list[tuple[int, int, int]] = []
    for prev, nxt in zip(rows, rows[1:]):
        d = kulonbseg(int(prev["szint"]), int(nxt["szint"]))
        out.append((d, int(prev["index"]), int(prev["ora"]) * 60 + int(prev["perc"])))
    return out


def _task_zsilip_count(rows: list[Row], _spec: dict[str, Any]) -> str:
    return f"A meresek szama: {len(rows)}"


def _task_zsilip_max(rows: list[Row], _spec: dict[str, Any]) -> str:
    jumps = _jumps(rows)
    peak = max(j[0] for j in jumps)
    best = min((j for j in jumps if j[0] == peak), key=lambda j: j[1])
    prev = rows[best[1] - 1]
    return f"A legnagyobb valtozas: {best[0]} cm, kezdete: {prev['ora']}:{prev['perc']}"


def _task_zsilip_riasztas(rows: list[Row], _spec: dict[str, Any]) -> str:
    if any(j[0] > 12 for j in _jumps(rows)):
        return "Volt riasztas."
    return "Nem volt riasztas."


def _find(rows: list[Row], ora: int, perc: int) -> int:
    for row in rows:
        if int(row["ora"]) == ora and int(row["perc"]) == perc:
            return int(row["szint"])
    raise KeyError((ora, perc))


def _task_zsilip_ketto(rows: list[Row], spec: dict[str, Any]) -> str:
    t = [int(x) for x in str(spec.get("stdin") or "").split()]
    a = _find(rows, t[0], t[1])
    b = _find(rows, t[2], t[3])
    d = kulonbseg(a, b)
    return (
        "Elso ora:\nElso perc:\nMasodik ora:\nMasodik perc:\n"
        f"A ket idopont kulonbsege: {d} cm"
    )


TASK_BUILDERS: dict[str, Callable[[list[Row], dict[str, Any]], str]] = {
    "zsilip_count": _task_zsilip_count,
    "zsilip_max": _task_zsilip_max,
    "zsilip_riasztas": _task_zsilip_riasztas,
    "zsilip_ketto": _task_zsilip_ketto,
}
