"""Oracle for Kompátkelő — students never see this module."""

from __future__ import annotations

from typing import Any, Callable

from app.exams.builders import Row, _nonempty_lines


def parse_kompatkelo(content: str) -> list[Row]:
    lines = _nonempty_lines(content)
    if not lines:
        return []
    cap = int(lines[0].split()[0])
    rows: list[Row] = []
    for i, line in enumerate(lines[1:], start=1):
        parts = line.split()
        rows.append(
            {
                "index": i,
                "jarat": int(parts[0]),
                "honap": int(parts[1]),
                "nap": int(parts[2]),
                "jarmu": int(parts[3]),
                "cel": parts[4],
                "kapacitas": cap,
            }
        )
    if not rows:
        rows.append({"index": 0, "jarat": 0, "jarmu": 0, "cel": "", "kapacitas": cap, "_empty": True})
    return rows


def parse(content: str) -> list[Row]:
    return parse_kompatkelo(content)


def _runs(rows: list[Row]) -> list[Row]:
    return [r for r in rows if r.get("index") and not r.get("_empty")]


def _task_kompatkelo_count(rows: list[Row], _spec: dict[str, Any]) -> str:
    return f"A jaratok szama: {len(_runs(rows))}"


def _task_kompatkelo_max(rows: list[Row], _spec: dict[str, Any]) -> str:
    runs = _runs(rows)
    peak = max(int(r["jarmu"]) for r in runs)
    best = min((r for r in runs if int(r["jarmu"]) == peak), key=lambda r: r["index"])
    return f"A legterheltebb jarat: {best['jarat']}, {best['jarmu']} jarmu, cel: {best['cel']}"


def _task_kompatkelo_group(rows: list[Row], _spec: dict[str, Any]) -> str:
    order: list[str] = []
    n: dict[str, int] = {}
    s: dict[str, int] = {}
    for row in _runs(rows):
        cel = str(row["cel"])
        if cel not in n:
            order.append(cel)
            n[cel] = 0
            s[cel] = 0
        n[cel] += 1
        s[cel] += int(row["jarmu"])
    return "\n".join(f"{cel} {n[cel]} {s[cel]}" for cel in order)


def _task_kompatkelo_cel(rows: list[Row], spec: dict[str, Any]) -> str:
    kod = str(spec.get("stdin") or "").strip().split()[0]
    lines = ["Adja meg a celallomas kodjat!"]
    hits = [r for r in _runs(rows) if r["cel"] == kod]
    if not hits:
        lines.append("Nincs ilyen celallomas.")
        return "\n".join(lines)
    lines.append(f"A jaratok szama: {len(hits)}")
    lines.append(f"A jarmuvek szama: {sum(int(r['jarmu']) for r in hits)}")
    return "\n".join(lines)


TASK_BUILDERS: dict[str, Callable[[list[Row], dict[str, Any]], str]] = {
    "kompatkelo_count": _task_kompatkelo_count,
    "kompatkelo_max": _task_kompatkelo_max,
    "kompatkelo_group": _task_kompatkelo_group,
    "kompatkelo_cel": _task_kompatkelo_cel,
}
