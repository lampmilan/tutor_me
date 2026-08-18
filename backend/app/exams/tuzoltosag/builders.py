"""Oracle for Tűzoltóság — students never see this module."""

from __future__ import annotations

from typing import Any, Callable

from app.exams.builders import Row, _nonempty_lines


def parse_tuzoltosag(content: str) -> list[Row]:
    rows: list[Row] = []
    for i, line in enumerate(_nonempty_lines(content), start=1):
        parts = line.split()
        rows.append(
            {
                "index": i,
                "ora": int(parts[0]),
                "perc": int(parts[1]),
                "kerulet": parts[2],
                "tipus": parts[3],
                "auto": int(parts[4]),
            }
        )
    return rows


def parse(content: str) -> list[Row]:
    return parse_tuzoltosag(content)


def _task_tuzoltosag_count(rows: list[Row], _spec: dict[str, Any]) -> str:
    return (
        f"A riasztasok szama: {len(rows)}\n"
        f"A kivonult autok szama: {sum(int(r['auto']) for r in rows)}"
    )


def _task_tuzoltosag_tuz(rows: list[Row], _spec: dict[str, Any]) -> str:
    n = sum(1 for r in rows if r["tipus"] == "TUZ")
    return f"A tuzesetek szama: {n}"


def _task_tuzoltosag_elso(rows: list[Row], _spec: dict[str, Any]) -> str:
    first = rows[0]
    return (
        f"Az elso riasztas: {first['ora']}:{first['perc']}, "
        f"kerulet: {first['kerulet']}, tipus: {first['tipus']}"
    )


def _task_tuzoltosag_kerulet(rows: list[Row], spec: dict[str, Any]) -> str:
    ker = str(spec.get("stdin") or "").strip().split()[0]
    lines = ["Adja meg a keruletet!"]
    hits = [r for r in rows if r["kerulet"] == ker]
    if not hits:
        lines.append("Nincs ilyen kerulet.")
        return "\n".join(lines)
    lines.append(f"A kerulet riasztasai: {len(hits)}")
    return "\n".join(lines)


def _task_tuzoltosag_file(rows: list[Row], _spec: dict[str, Any]) -> str:
    return "\n".join(
        f"{r['ora']} {r['perc']} {r['kerulet']} {r['auto']}"
        for r in rows
        if r["tipus"] == "TUZ"
    )


TASK_BUILDERS: dict[str, Callable[[list[Row], dict[str, Any]], str]] = {
    "tuzoltosag_count": _task_tuzoltosag_count,
    "tuzoltosag_tuz": _task_tuzoltosag_tuz,
    "tuzoltosag_elso": _task_tuzoltosag_elso,
    "tuzoltosag_kerulet": _task_tuzoltosag_kerulet,
    "tuzoltosag_file": _task_tuzoltosag_file,
}
