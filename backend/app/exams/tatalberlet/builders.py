"""Oracle for Tatalbérlet — students never see this module."""

from __future__ import annotations

from typing import Any, Callable

from app.exams.builders import Row, _nonempty_lines


def pontszam(berleti_dij: int, alapterulet: int) -> float:
    return alapterulet / berleti_dij * 10


def parse_tatalberlet(content: str) -> list[Row]:
    rows: list[Row] = []
    for line in _nonempty_lines(content):
        parts = line.split()
        if len(parts) < 5:
            raise ValueError(f"Invalid tatalberlet line: {line!r}")
        sorszam, dij, terulet, haziallat, tipus = parts[0], parts[1], parts[2], parts[3], parts[4]
        rows.append(
            {
                "sorszam": int(sorszam),
                "dij": int(dij),
                "terulet": int(terulet),
                "haziallat": haziallat,
                "tipus": tipus,
            }
        )
    return rows


def parse(content: str) -> list[Row]:
    return parse_tatalberlet(content)


def _pet_rows(rows: list[Row]) -> list[Row]:
    return [r for r in rows if r["haziallat"] == "igen"]


def _stdin_int(spec: dict[str, Any], default: str = "0") -> int:
    return int(str(spec.get("stdin") or default).strip().split()[0])


def _task_tatalberlet_haziallatos_szama(rows: list[Row], _spec: dict[str, Any]) -> str:
    return f"Haziallatos berletek szama: {len(_pet_rows(rows))}"


def _task_tatalberlet_legolcsobb(rows: list[Row], _spec: dict[str, Any]) -> str:
    pets = _pet_rows(rows)
    best_dij = min(int(r["dij"]) for r in pets)
    best = min((r for r in pets if int(r["dij"]) == best_dij), key=lambda r: r["sorszam"])
    return (
        f"Legolcsobb haziallatos: {best['sorszam']}. "
        f"berleti dij: {best['dij']} eFt, alapterulet: {best['terulet']} m2"
    )


def _task_tatalberlet_kereses(rows: list[Row], spec: dict[str, Any]) -> str:
    wanted = _stdin_int(spec, "1")
    lines = ["Adja meg a berleti sorszamat!"]
    hit = next((r for r in rows if r["sorszam"] == wanted), None)
    if hit is None:
        lines.append("Nem talalhato ilyen berleti.")
        return "\n".join(lines)
    lines.extend(
        [
            f"Berleti dij: {hit['dij']} eFt",
            f"Alapterulet: {hit['terulet']} m2",
            f"Tipus: {hit['tipus']}",
            f"Haziallat: {hit['haziallat']}",
        ]
    )
    return "\n".join(lines)


def _affordable_pets(rows: list[Row], budget: int) -> list[Row]:
    return [r for r in _pet_rows(rows) if int(r["dij"]) <= budget]


def _best_pet_choice(rows: list[Row], budget: int) -> Row | None:
    candidates = _affordable_pets(rows, budget)
    if not candidates:
        return None
    return max(
        candidates,
        key=lambda r: (pontszam(int(r["dij"]), int(r["terulet"])), -int(r["sorszam"])),
    )


def _task_tatalberlet_legjobb(rows: list[Row], spec: dict[str, Any]) -> str:
    budget = _stdin_int(spec, "100")
    lines = ["Havi budzse (eFt)!"]
    best = _best_pet_choice(rows, budget)
    if best is None:
        lines.append("Sajnos egy haziallatos berletet sem engedhetsz meg magadnak, Nolan.")
        return "\n".join(lines)
    score = pontszam(int(best["dij"]), int(best["terulet"]))
    lines.append(f"Legjobb valasztas: {best['sorszam']}. pontszam: {score:.1f}")
    return "\n".join(lines)


def _task_tatalberlet_megfizetheto(rows: list[Row], spec: dict[str, Any]) -> str:
    budget = _stdin_int(spec, "100")
    affordable = [r for r in rows if int(r["dij"]) <= budget]
    affordable.sort(
        key=lambda r: (pontszam(int(r["dij"]), int(r["terulet"])), -int(r["sorszam"])),
        reverse=True,
    )
    return "\n".join(
        f"{r['sorszam']} {r['dij']} {r['terulet']} {r['tipus']} {r['haziallat']}"
        for r in affordable
    )


TASK_BUILDERS: dict[str, Callable[[list[Row], dict[str, Any]], str]] = {
    "tatalberlet_haziallatos_szama": _task_tatalberlet_haziallatos_szama,
    "tatalberlet_legolcsobb": _task_tatalberlet_legolcsobb,
    "tatalberlet_kereses": _task_tatalberlet_kereses,
    "tatalberlet_legjobb": _task_tatalberlet_legjobb,
    "tatalberlet_megfizetheto": _task_tatalberlet_megfizetheto,
}
