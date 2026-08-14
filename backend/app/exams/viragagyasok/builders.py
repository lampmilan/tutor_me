"""Oracle for Virágágyások — students never see this module.

Student runtime gets the file as a raw string via the preamble.
Expected outputs are still derived from parsed rows.
"""

from __future__ import annotations

from typing import Any, Callable

from app.exams.builders import Row, _nonempty_lines


def parse(content: str) -> list[Row]:
    """Flower-bed offers: first line is bed count, then start end color."""
    lines = _nonempty_lines(content)
    if not lines:
        return []
    n_beds = int(lines[0])
    rows: list[Row] = []
    for i, line in enumerate(lines[1:], start=1):
        parts = line.split()
        if len(parts) < 3:
            raise ValueError(f"Invalid viragagyasok line: {line!r}")
        rows.append(
            {
                "index": i,
                "start": int(parts[0]),
                "end": int(parts[1]),
                "color": parts[2],
                "n_beds": n_beds,
            }
        )
    if not rows:
        rows.append({"index": 0, "start": 0, "end": 0, "color": "", "n_beds": n_beds, "_empty": True})
    return rows


def _offers(rows: list[Row]) -> list[Row]:
    return [r for r in rows if r.get("index") and not r.get("_empty")]


def _n_beds(rows: list[Row]) -> int:
    if not rows:
        return 0
    return int(rows[0]["n_beds"])


def _iter_beds(start: int, end: int, n: int) -> list[int]:
    if start <= end:
        return list(range(start, end + 1))
    return list(range(start, n + 1)) + list(range(1, end + 1))


def _covers(start: int, end: int, bed: int) -> bool:
    if start <= end:
        return start <= bed <= end
    return bed >= start or bed <= end


def _interval_len(start: int, end: int, n: int) -> int:
    if start <= end:
        return end - start + 1
    return n - start + 1 + end


def _bed_from_spec(spec: dict[str, Any]) -> int:
    raw = str(spec.get("stdin") or "1").strip().split()[0]
    return int(raw)


def _task_offer_count(rows: list[Row], _spec: dict[str, Any]) -> str:
    return f"A felajánlások száma: {len(_offers(rows))}"


def _task_wrap_offers(rows: list[Row], _spec: dict[str, Any]) -> str:
    ids = [str(r["index"]) for r in _offers(rows) if int(r["start"]) > int(r["end"])]
    return "A bejárat mindkét oldalán ültetők: " + " ".join(ids)


def _task_bed_query(rows: list[Row], spec: dict[str, Any]) -> str:
    bed = _bed_from_spec(spec)
    hits = [r for r in _offers(rows) if _covers(int(r["start"]), int(r["end"]), bed)]
    lines = [
        "Adja meg az ágyás sorszámát!",
        f"A felajánlók száma: {len(hits)}",
    ]
    if not hits:
        lines.append("Ezt az ágyást nem ültetik be.")
        return "\n".join(lines)
    lines.append(f"A virágágyás színe, ha csak az első ültet: {hits[0]['color']}")
    unique: list[str] = []
    for row in hits:
        color = str(row["color"])
        if color not in unique:
            unique.append(color)
    lines.append("A virágágyás színei: " + " ".join(unique))
    return "\n".join(lines)


def _task_planting_status(rows: list[Row], _spec: dict[str, Any]) -> str:
    n = _n_beds(rows)
    covered: set[int] = set()
    pledged = 0
    for row in _offers(rows):
        start, end = int(row["start"]), int(row["end"])
        pledged += _interval_len(start, end, n)
        covered.update(_iter_beds(start, end, n))
    if n and len(covered) == n:
        return "Minden ágyás beültetésére van jelentkező."
    if pledged >= n:
        return "Átszervezéssel megoldható a beültetés."
    return "A beültetés nem oldható meg."


def _task_colors_file(rows: list[Row], _spec: dict[str, Any]) -> str:
    n = _n_beds(rows)
    colors = ["#"] * n
    who = [0] * n
    for row in _offers(rows):
        idx = int(row["index"])
        start, end = int(row["start"]), int(row["end"])
        color = str(row["color"])
        for bed in _iter_beds(start, end, n):
            pos = bed - 1
            if colors[pos] == "#":
                colors[pos] = color
                who[pos] = idx
    return "\n".join(f"{c} {w}" for c, w in zip(colors, who))


TASK_BUILDERS: dict[str, Callable[[list[Row], dict[str, Any]], str]] = {
    "offer_count": _task_offer_count,
    "wrap_offers": _task_wrap_offers,
    "bed_query": _task_bed_query,
    "planting_status": _task_planting_status,
    "colors_file": _task_colors_file,
}
