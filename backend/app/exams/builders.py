"""Dataset parsers and task expected-output builders.

Expected outputs are always derived from dataset contents + task type —
never authored as a separate field in templates.
"""

from __future__ import annotations

from typing import Any, Callable

Row = dict[str, Any]


def _nonempty_lines(content: str) -> list[str]:
    return [line.strip() for line in content.splitlines() if line.strip()]


def parse_cities(content: str) -> list[Row]:
    rows: list[Row] = []
    for line in _nonempty_lines(content):
        parts = line.split()
        if len(parts) < 2:
            raise ValueError(f"Invalid cities line: {line!r}")
        name, pop = parts[0], int(parts[1])
        rows.append({"name": name, "population": pop})
    return rows


def parse_trains(content: str) -> list[Row]:
    rows: list[Row] = []
    for line in _nonempty_lines(content):
        parts = line.split()
        if len(parts) < 4:
            raise ValueError(f"Invalid trains line: {line!r}")
        rows.append(
            {
                "id": parts[0],
                "from": parts[1],
                "to": parts[2],
                "minutes": int(parts[3]),
            }
        )
    return rows


def parse_temperatures(content: str) -> list[Row]:
    rows: list[Row] = []
    for line in _nonempty_lines(content):
        parts = line.split()
        if len(parts) < 2:
            raise ValueError(f"Invalid temperatures line: {line!r}")
        rows.append({"date": parts[0], "celsius": int(parts[1])})
    return rows


def parse_students(content: str) -> list[Row]:
    rows: list[Row] = []
    for line in _nonempty_lines(content):
        parts = line.split()
        if len(parts) < 2:
            raise ValueError(f"Invalid students line: {line!r}")
        rows.append({"name": parts[0], "grade": int(parts[1])})
    return rows


def parse_lines(content: str) -> list[Row]:
    """Raw non-empty lines (for free-form text files such as MRZ)."""
    return [{"text": line, "index": i} for i, line in enumerate(_nonempty_lines(content), start=1)]


def parse_viragagyasok(content: str) -> list[Row]:
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


PARSERS: dict[str, Callable[[str], list[Row]]] = {
    "cities": parse_cities,
    "trains": parse_trains,
    "temperatures": parse_temperatures,
    "students": parse_students,
    "lines": parse_lines,
    "viragagyasok": parse_viragagyasok,
}


def parse_dataset(dataset_type: str, content: str) -> list[Row]:
    parser = PARSERS.get(dataset_type)
    if not parser:
        raise ValueError(f"Unsupported dataset type: {dataset_type}")
    return parser(content)


def _task_count(rows: list[Row], _spec: dict[str, Any]) -> str:
    return str(len(rows))


def _task_maximum(rows: list[Row], spec: dict[str, Any]) -> str:
    field = spec.get("field")
    if not field:
        raise ValueError("maximum task requires 'field'")
    best = max(rows, key=lambda r: r[field])
    label_field = spec.get("label_field")
    if label_field:
        return str(best[label_field])
    return str(best[field])


def _task_minimum(rows: list[Row], spec: dict[str, Any]) -> str:
    field = spec.get("field")
    if not field:
        raise ValueError("minimum task requires 'field'")
    best = min(rows, key=lambda r: r[field])
    label_field = spec.get("label_field")
    if label_field:
        return str(best[label_field])
    return str(best[field])


def _task_sum(rows: list[Row], spec: dict[str, Any]) -> str:
    field = spec.get("field")
    if not field:
        raise ValueError("sum task requires 'field'")
    return str(sum(r[field] for r in rows))


def _task_average(rows: list[Row], spec: dict[str, Any]) -> str:
    field = spec.get("field")
    if not field:
        raise ValueError("average task requires 'field'")
    if not rows:
        return "0"
    return str(int(sum(r[field] for r in rows) / len(rows)))


def _compare(actual: Any, op: str, expected: Any) -> bool:
    if op == "eq":
        return actual == expected
    if op == "gte":
        return actual >= expected
    if op == "lte":
        return actual <= expected
    if op == "gt":
        return actual > expected
    if op == "lt":
        return actual < expected
    raise ValueError(f"Unsupported op: {op}")


def _coerce(value: Any, sample: Any) -> Any:
    if isinstance(sample, int):
        return int(value)
    if isinstance(sample, float):
        return float(value)
    return value


def _task_count_where(rows: list[Row], spec: dict[str, Any]) -> str:
    field = spec.get("field")
    op = spec.get("op", "eq")
    if field is None or "value" not in spec:
        raise ValueError("count_where task requires 'field' and 'value'")
    if not rows:
        return "0"
    target = _coerce(spec["value"], rows[0][field])
    return str(sum(1 for r in rows if _compare(r[field], op, target)))


def _format_row(row: Row, dataset_hint: str | None = None) -> str:
    """Best-effort line dump for 'read' tasks (echo dataset content)."""
    if "text" in row and len(row) <= 2:
        return str(row["text"])
    if "name" in row and "population" in row:
        return f"{row['name']} {row['population']}"
    if "id" in row and "from" in row and "to" in row and "minutes" in row:
        return f"{row['id']} {row['from']} {row['to']} {row['minutes']}"
    if "date" in row and "celsius" in row:
        return f"{row['date']} {row['celsius']}"
    if "name" in row and "grade" in row:
        return f"{row['name']} {row['grade']}"
    # Fallback: stable key order
    return " ".join(str(row[k]) for k in sorted(row.keys()))


def _task_read(rows: list[Row], _spec: dict[str, Any]) -> str:
    return "\n".join(_format_row(r) for r in rows)


def _task_literal(_rows: list[Row], spec: dict[str, Any]) -> str:
    """Authored expected output (preview / non-derivable feladat text)."""
    if "value" not in spec:
        raise ValueError("literal task requires 'value'")
    return str(spec["value"])


def _task_store(_rows: list[Row], _spec: dict[str, Any]) -> str:
    """Load-only feladat: no required stdout."""
    return ""


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
    "read": _task_read,
    "count": _task_count,
    "maximum": _task_maximum,
    "minimum": _task_minimum,
    "sum": _task_sum,
    "average": _task_average,
    "count_where": _task_count_where,
    "literal": _task_literal,
    "store": _task_store,
    "offer_count": _task_offer_count,
    "wrap_offers": _task_wrap_offers,
    "bed_query": _task_bed_query,
    "planting_status": _task_planting_status,
    "colors_file": _task_colors_file,
}


def expected_for_task(rows: list[Row], task_spec: dict[str, Any]) -> str:
    ttype = task_spec.get("type", "count")
    builder = TASK_BUILDERS.get(ttype)
    if not builder:
        raise ValueError(f"Unknown task type: {ttype}")
    return builder(rows, task_spec)
