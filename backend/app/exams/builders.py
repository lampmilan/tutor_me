"""Shared dataset parsers and generic task expected-output builders.

Expected outputs are always derived from dataset contents + task type —
never authored as a separate field in templates.

Exam-specific oracles live next to the exam:
`backend/app/exams/<id>/builders.py` (loaded by path; folder names may contain hyphens).

Student runtime is independent of this module: later feladats get a raw file
string via `raw_file_preamble()`, then split/convert it themselves.
"""

from __future__ import annotations

import importlib.util
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

Row = dict[str, Any]


@dataclass
class ExamPlugin:
    """Optional per-exam parse + task builders (students never see this)."""

    parse: Callable[[str], list[Row]] | None = None
    task_builders: dict[str, Callable[[list[Row], dict[str, Any]], str]] = field(
        default_factory=dict
    )


def raw_file_preamble(data_file: str, shared_variable: str) -> str:
    """Canonical later-feladat inject: file contents as str, read at runtime."""
    return (
        f'with open("{data_file}", encoding="utf-8") as f:\n'
        f"    {shared_variable} = f.read()\n"
    )


def load_exam_plugin(exam_dir: Path) -> ExamPlugin | None:
    path = exam_dir / "builders.py"
    if not path.is_file():
        return None
    mod_name = f"app.exams._plugin_{exam_dir.name.replace('-', '_')}"
    spec = importlib.util.spec_from_file_location(mod_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load exam plugin: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[mod_name] = module
    spec.loader.exec_module(module)
    builders = getattr(module, "TASK_BUILDERS", None) or {}
    return ExamPlugin(
        parse=getattr(module, "parse", None),
        task_builders=dict(builders),
    )


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


PARSERS: dict[str, Callable[[str], list[Row]]] = {
    "cities": parse_cities,
    "trains": parse_trains,
    "temperatures": parse_temperatures,
    "students": parse_students,
    "lines": parse_lines,
}


def parse_dataset(
    dataset_type: str,
    content: str,
    *,
    plugin: ExamPlugin | None = None,
) -> list[Row]:
    if plugin and plugin.parse is not None:
        return plugin.parse(content)
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
    del dataset_hint
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
}


def expected_for_task(
    rows: list[Row],
    task_spec: dict[str, Any],
    *,
    plugin: ExamPlugin | None = None,
) -> str:
    ttype = task_spec.get("type", "count")
    if plugin and ttype in plugin.task_builders:
        return plugin.task_builders[ttype](rows, task_spec)
    builder = TASK_BUILDERS.get(ttype)
    if not builder:
        raise ValueError(f"Unknown task type: {ttype}")
    return builder(rows, task_spec)
