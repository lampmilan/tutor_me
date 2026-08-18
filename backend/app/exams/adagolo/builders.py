"""Oracle for Adagoló — students never see this module."""

from __future__ import annotations

from typing import Any, Callable

from app.exams.builders import Row, _nonempty_lines


def parse_adagolo(content: str) -> list[Row]:
    patients: list[list[tuple[str, int]]] = []
    cur: list[tuple[str, int]] = []
    for line in _nonempty_lines(content):
        if line == "X":
            patients.append(cur)
            cur = []
        else:
            name, n = line.split()
            cur.append((name, int(n)))
    rows: list[Row] = []
    for pi, items in enumerate(patients, start=1):
        total = sum(n for _name, n in items)
        for name, n in items:
            rows.append(
                {
                    "patient": pi,
                    "name": name,
                    "db": n,
                    "patient_total": total,
                    "n_patients": len(patients),
                    "totals": [sum(x for _k, x in p) for p in patients],
                }
            )
    return rows


def parse(content: str) -> list[Row]:
    return parse_adagolo(content)


def _totals(rows: list[Row]) -> list[int]:
    return list(rows[0]["totals"]) if rows else []


def _task_adagolo_count(rows: list[Row], _spec: dict[str, Any]) -> str:
    n = int(rows[0]["n_patients"]) if rows else 0
    return f"A betegek szama: {n}"


def _task_adagolo_max(rows: list[Row], _spec: dict[str, Any]) -> str:
    totals = _totals(rows)
    peak = max(totals)
    idx = totals.index(peak) + 1
    return f"Az osszes doboz: {sum(totals)}\nA legnagyobb adag: {idx}. beteg, {peak} doboz"


def _task_adagolo_nev(rows: list[Row], spec: dict[str, Any]) -> str:
    nev = str(spec.get("stdin") or "").strip().split()[0]
    lines = ["Adja meg a keszitmeny nevet!"]
    hits = [r for r in rows if r["name"] == nev]
    if not hits:
        lines.append("Nincs ilyen keszitmeny.")
        return "\n".join(lines)
    lines.append(f"A kiadott dobozok szama: {sum(int(r['db']) for r in hits)}")
    return "\n".join(lines)


def _task_adagolo_file(rows: list[Row], _spec: dict[str, Any]) -> str:
    totals = _totals(rows)
    return "\n".join(f"{i} {t}" for i, t in enumerate(totals, start=1))


TASK_BUILDERS: dict[str, Callable[[list[Row], dict[str, Any]], str]] = {
    "adagolo_count": _task_adagolo_count,
    "adagolo_max": _task_adagolo_max,
    "adagolo_nev": _task_adagolo_nev,
    "adagolo_file": _task_adagolo_file,
}
