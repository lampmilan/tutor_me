"""Oracle for MRZ kód — students never see this module.

Student runtime gets mrz.txt as a raw string via the preamble.
"""

from __future__ import annotations

from typing import Any, Callable

from app.exams.builders import Row, parse_lines


def parse(content: str) -> list[Row]:
    return parse_lines(content)


def _line(rows: list[Row], index: int) -> str:
    if index < 0 or index >= len(rows):
        return ""
    row = rows[index]
    if "text" in row:
        return str(row["text"])
    return ""


def _task_gender(rows: list[Row], _spec: dict[str, Any]) -> str:
    second = _line(rows, 1)
    if len(second) < 21:
        return ""
    gender = second[20]
    if gender == "F":
        return "Az okmány tulajdonosa nő."
    if gender == "M":
        return "Az okmány tulajdonosa férfi."
    return ""


def _task_mrz_name(rows: list[Row], _spec: dict[str, Any]) -> str:
    first = _line(rows, 0)
    if len(first) < 6:
        return ""
    name_field = first[5:44] if len(first) >= 44 else first[5:]
    truncated = not first.endswith("<")
    if "<<" in name_field:
        family_raw, given_raw = name_field.split("<<", 1)
    else:
        family_raw, given_raw = name_field, ""
    family = " ".join(part for part in family_raw.split("<") if part)
    given = " ".join(part for part in given_raw.split("<") if part)
    status = (
        "Lehetséges, hogy csonkolt a név." if truncated else "A név nem csonkolt."
    )
    return f"Családi név: {family}\nUtónév: {given}\n{status}"


TASK_BUILDERS: dict[str, Callable[[list[Row], dict[str, Any]], str]] = {
    "gender": _task_gender,
    "mrz_name": _task_mrz_name,
}
