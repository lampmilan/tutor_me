"""Oracle for Csomagfeladás — students never see this module."""

from __future__ import annotations

from typing import Any, Callable

from app.exams.builders import Row, _nonempty_lines


def parse_csomagfeladas(content: str) -> list[Row]:
    rows: list[Row] = []
    for i, line in enumerate(_nonempty_lines(content), start=1):
        parts = line.split()
        rows.append({"index": i, "max_kg": int(parts[0]), "dij": int(parts[1])})
    return rows


def parse(content: str) -> list[Row]:
    return parse_csomagfeladas(content)


def _fee(rows: list[Row], weight: int) -> int:
    ordered = sorted(rows, key=lambda r: int(r["max_kg"]))
    for row in ordered:
        if weight <= int(row["max_kg"]):
            return int(row["dij"])
    return int(ordered[-1]["dij"])


def _weights(spec: dict[str, Any]) -> list[int]:
    tokens = [int(t) for t in str(spec.get("stdin") or "").split()]
    out: list[int] = []
    for w in tokens:
        if w == 0:
            break
        out.append(w)
    return out


def _task_csomagfeladas_count(rows: list[Row], _spec: dict[str, Any]) -> str:
    return f"A dijkategoriak szama: {len(rows)}"


def _task_csomagfeladas_feladas(rows: list[Row], spec: dict[str, Any]) -> str:
    weights = _weights(spec)
    lines: list[str] = []
    total = 0
    for w in weights:
        dij = _fee(rows, w)
        total += dij
        lines.append("Csomag tomege (kg):")
        lines.append(f"Dij: {dij} Ft")
    lines.append("Csomag tomege (kg):")
    lines.append(f"Osszesen: {total} Ft")
    return "\n".join(lines)


TASK_BUILDERS: dict[str, Callable[[list[Row], dict[str, Any]], str]] = {
    "csomagfeladas_count": _task_csomagfeladas_count,
    "csomagfeladas_feladas": _task_csomagfeladas_feladas,
}
