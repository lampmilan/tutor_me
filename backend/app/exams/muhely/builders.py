"""Oracle for Műhely — students never see this module."""

from __future__ import annotations

from collections import defaultdict
from typing import Any, Callable

from app.exams.builders import Row, _nonempty_lines


def parse_muhely(content: str) -> list[Row]:
    rows: list[Row] = []
    for i, line in enumerate(_nonempty_lines(content), start=1):
        parts = line.split()
        rows.append(
            {
                "index": i,
                "ora": int(parts[0]),
                "perc": int(parts[1]),
                "muvelet": parts[2],
                "szerszam": int(parts[3]),
                "percben": int(parts[0]) * 60 + int(parts[1]),
            }
        )
    return rows


def parse(content: str) -> list[Row]:
    return parse_muhely(content)


def _closed_and_open(rows: list[Row]) -> tuple[list[tuple[int, int, int]], set[int]]:
    stacks: dict[int, list[tuple[int, int]]] = defaultdict(list)
    closed: list[tuple[int, int, int]] = []  # (duration, start_index, tool)
    for row in rows:
        tid = int(row["szerszam"])
        if row["muvelet"] == "KI":
            stacks[tid].append((int(row["percben"]), int(row["index"])))
        else:
            start_min, start_idx = stacks[tid].pop()
            closed.append((int(row["percben"]) - start_min, start_idx, tid))
    still = {tid for tid, st in stacks.items() if st}
    return closed, still


def _task_muhely_count(rows: list[Row], _spec: dict[str, Any]) -> str:
    return f"A kolcsonzesi esemenyek szama: {len(rows)}"


def _task_muhely_kint(rows: list[Row], _spec: dict[str, Any]) -> str:
    _closed, still = _closed_and_open(rows)
    ids = " ".join(str(t) for t in sorted(still))
    return f"A kint maradt szerszamok szama: {len(still)}\nA kint maradt azonosito: {ids}"


def _task_muhely_max(rows: list[Row], _spec: dict[str, Any]) -> str:
    closed, _still = _closed_and_open(rows)
    peak = max(c[0] for c in closed)
    best = min((c for c in closed if c[0] == peak), key=lambda c: c[1])
    return f"A leghosszabb kolcsonzes: {best[0]} perc, szerszam: {best[2]}"


def _task_muhely_szerszam(rows: list[Row], spec: dict[str, Any]) -> str:
    tid = int(str(spec.get("stdin") or "0").strip().split()[0])
    lines = ["Adja meg a szerszam azonositojat!"]
    if all(int(r["szerszam"]) != tid for r in rows):
        lines.append("Nincs ilyen szerszam.")
        return "\n".join(lines)
    closed, _still = _closed_and_open(rows)
    mine = [c for c in closed if c[2] == tid]
    lines.append(f"A lezart kolcsonzesek szama: {len(mine)}")
    lines.append(f"A kolcsonzesek osszideje: {sum(c[0] for c in mine)} perc")
    return "\n".join(lines)


TASK_BUILDERS: dict[str, Callable[[list[Row], dict[str, Any]], str]] = {
    "muhely_count": _task_muhely_count,
    "muhely_kint": _task_muhely_kint,
    "muhely_max": _task_muhely_max,
    "muhely_szerszam": _task_muhely_szerszam,
}
