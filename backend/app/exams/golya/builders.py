"""Oracle for Gólya — students never see this module."""

from __future__ import annotations

from typing import Any, Callable

from app.exams.builders import Row, _nonempty_lines


def tavolsag(x1: int, y1: int, x2: int, y2: int) -> float:
    return ((int(x1) - int(x2)) ** 2 + (int(y1) - int(y2)) ** 2) ** 0.5


def parse_golya(content: str) -> list[Row]:
    rows: list[Row] = []
    for i, line in enumerate(_nonempty_lines(content), start=1):
        parts = line.split()
        if len(parts) < 5:
            raise ValueError(f"Invalid golya line: {line!r}")
        honap, nap, x, y, orszag = parts[0], parts[1], parts[2], parts[3], " ".join(parts[4:])
        rows.append(
            {
                "index": i,
                "honap": int(honap),
                "nap": int(nap),
                "x": int(x),
                "y": int(y),
                "orszag": orszag,
            }
        )
    return rows


def parse(content: str) -> list[Row]:
    return parse_golya(content)


def _fmt_date(row: Row) -> str:
    return f"{row['honap']}.{row['nap']}"


def _country_order(rows: list[Row]) -> list[str]:
    seen: list[str] = []
    for row in rows:
        name = str(row["orszag"])
        if name not in seen:
            seen.append(name)
    return seen


def _days_by_country(rows: list[Row]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in rows:
        name = str(row["orszag"])
        counts[name] = counts.get(name, 0) + 1
    return counts


def _stdin_token(spec: dict[str, Any]) -> str:
    return str(spec.get("stdin") or "").strip().split()[0] if str(spec.get("stdin") or "").strip() else ""


def _task_golya_count(rows: list[Row], _spec: dict[str, Any]) -> str:
    return f"A meresek szama: {len(rows)}"


def _task_golya_orszagok(rows: list[Row], _spec: dict[str, Any]) -> str:
    order = _country_order(rows)
    return (
        f"A vonulas kezdete: {rows[0]['orszag']}\n"
        f"A vonulas vege: {rows[-1]['orszag']}\n"
        f"Az erintett orszagok szama: {len(order)}"
    )


def _task_golya_orszag(rows: list[Row], spec: dict[str, Any]) -> str:
    name = _stdin_token(spec)
    lines = ["Adja meg az orszag nevet!"]
    hits = [r for r in rows if r["orszag"] == name]
    if not hits:
        lines.append("Zsiga nem jart ebben az orszagban.")
        return "\n".join(lines)
    lines.append(f"Zsiga ebben az orszagban {len(hits)} napot toltott.")
    lines.append(f"Eloszor: {_fmt_date(hits[0])}")
    lines.append(f"Utoljara: {_fmt_date(hits[-1])}")
    return "\n".join(lines)


def _task_golya_max_hop(rows: list[Row], _spec: dict[str, Any]) -> str:
    best_d = -1.0
    best_start: Row = rows[0]
    for prev, cur in zip(rows, rows[1:]):
        d = tavolsag(prev["x"], prev["y"], cur["x"], cur["y"])
        if d > best_d:
            best_d = d
            best_start = prev
    return (
        f"A legnagyobb napi tavolsag: {round(best_d, 3):.3f}\n"
        f"A repules napja: {_fmt_date(best_start)}"
    )


def _task_golya_max_orszag(rows: list[Row], _spec: dict[str, Any]) -> str:
    counts = _days_by_country(rows)
    peak = max(counts.values())
    winner = next(name for name in _country_order(rows) if counts[name] == peak)
    return f"A legtobb nap: {winner}, {peak} nap"


def _task_golya_hatar(rows: list[Row], _spec: dict[str, Any]) -> str:
    out: list[str] = []
    for prev, cur in zip(rows, rows[1:]):
        if prev["orszag"] != cur["orszag"]:
            out.append(f"{cur['honap']} {cur['nap']} {prev['orszag']} {cur['orszag']}")
    return "\n".join(out)


TASK_BUILDERS: dict[str, Callable[[list[Row], dict[str, Any]], str]] = {
    "golya_count": _task_golya_count,
    "golya_orszagok": _task_golya_orszagok,
    "golya_orszag": _task_golya_orszag,
    "golya_max_hop": _task_golya_max_hop,
    "golya_max_orszag": _task_golya_max_orszag,
    "golya_hatar": _task_golya_hatar,
}
