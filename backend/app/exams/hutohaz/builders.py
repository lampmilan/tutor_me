"""Oracle for Hűtőház — students never see this module."""

from __future__ import annotations

from typing import Any, Callable

from app.exams.builders import Row, _nonempty_lines

KAPACITAS = 70


def percben(ora: int, perc: int) -> int:
    return int(ora) * 60 + int(perc)


def parse_hutohaz(content: str) -> list[Row]:
    rows: list[Row] = []
    for i, line in enumerate(_nonempty_lines(content), start=1):
        parts = line.split()
        if len(parts) < 5:
            raise ValueError(f"Invalid hutohaz line: {line!r}")
        ora, perc, muvelet, termek, ladak = parts[0], parts[1], parts[2], parts[3], parts[4]
        rows.append(
            {
                "index": i,
                "ora": int(ora),
                "perc": int(perc),
                "muvelet": muvelet,
                "termek": termek,
                "ladak": int(ladak),
                "percben": percben(int(ora), int(perc)),
            }
        )
    return rows


def parse(content: str) -> list[Row]:
    return parse_hutohaz(content)


def _stock_after(rows: list[Row], upto_inclusive: int | None = None) -> int:
    total = 0
    for row in rows:
        if upto_inclusive is not None and int(row["percben"]) > upto_inclusive:
            break
        if row["muvelet"] == "BE":
            total += int(row["ladak"])
        else:
            total -= int(row["ladak"])
    return total


def _task_hutohaz_count(rows: list[Row], _spec: dict[str, Any]) -> str:
    return f"A rakodasi esemenyek szama: {len(rows)}"


def _task_hutohaz_max_be(rows: list[Row], _spec: dict[str, Any]) -> str:
    bes = [r for r in rows if r["muvelet"] == "BE"]
    peak = max(int(r["ladak"]) for r in bes)
    best = min((r for r in bes if int(r["ladak"]) == peak), key=lambda r: r["index"])
    return f"A legnagyobb beszallitas: {best['ladak']} lada, termek: {best['termek']}"


def _stdin_tokens(spec: dict[str, Any]) -> list[str]:
    return str(spec.get("stdin") or "").split()


def _task_hutohaz_keszlet(rows: list[Row], spec: dict[str, Any]) -> str:
    tokens = _stdin_tokens(spec)
    ora, perc = int(tokens[0]), int(tokens[1])
    stock = _stock_after(rows, percben(ora, perc))
    return f"Ora:\nPerc:\nA hutohazban ekkor {stock} lada volt."


def _task_hutohaz_termek(rows: list[Row], spec: dict[str, Any]) -> str:
    name = _stdin_tokens(spec)[0]
    lines = ["Adja meg a termek nevet!"]
    hits = [r for r in rows if r["termek"] == name]
    if not hits:
        lines.append("Nincs ilyen termek.")
        return "\n".join(lines)
    be_n = sum(1 for r in hits if r["muvelet"] == "BE")
    closing = 0
    for row in hits:
        closing += int(row["ladak"]) if row["muvelet"] == "BE" else -int(row["ladak"])
    lines.append(f"A beszallitasok szama: {be_n}")
    lines.append(f"A zaro keszlet: {closing} lada")
    return "\n".join(lines)


def _first_overflow(rows: list[Row]) -> tuple[int, int] | None:
    total = 0
    for row in rows:
        if row["muvelet"] == "BE":
            total += int(row["ladak"])
        else:
            total -= int(row["ladak"])
        if total > KAPACITAS:
            return int(row["ora"]), int(row["perc"])
    return None


def _task_hutohaz_kapacitas(rows: list[Row], _spec: dict[str, Any]) -> str:
    hit = _first_overflow(rows)
    if hit is None:
        return "A hűtőház a nap folyamán végig a kapacitáson belül maradt."
    ora, perc = hit
    return (
        "A hűtőház legalább egyszer túllépte a kapacitást.\n"
        f"Az elso tullepes idopontja: {ora}:{perc}"
    )


def _task_hutohaz_keszlet_file(rows: list[Row], _spec: dict[str, Any]) -> str:
    total = 0
    out: list[str] = []
    for row in rows:
        if row["muvelet"] == "BE":
            total += int(row["ladak"])
        else:
            total -= int(row["ladak"])
        out.append(f"{row['ora']} {row['perc']} {total}")
    return "\n".join(out)


TASK_BUILDERS: dict[str, Callable[[list[Row], dict[str, Any]], str]] = {
    "hutohaz_count": _task_hutohaz_count,
    "hutohaz_max_be": _task_hutohaz_max_be,
    "hutohaz_keszlet": _task_hutohaz_keszlet,
    "hutohaz_termek": _task_hutohaz_termek,
    "hutohaz_kapacitas": _task_hutohaz_kapacitas,
    "hutohaz_keszlet_file": _task_hutohaz_keszlet_file,
}
