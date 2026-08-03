"""Exam template engine.

Templates define grading logic and task types.
AI (Phase 8) may only rewrite story text and generate realistic data —
never grading rules.
"""

from __future__ import annotations

import json
import random
from typing import Any

from sqlalchemy.orm import Session

from app.models import Exam, ExamFile, Task, TestCase
from app.services import ai_generator


# Built-in Hungarian city names for dataset generation
DEFAULT_CITIES = [
    ("Budapest", 1780000),
    ("Debrecen", 200000),
    ("Szeged", 160000),
    ("Miskolc", 150000),
    ("Pecs", 140000),
    ("Gyor", 130000),
    ("Nyiregyhaza", 116000),
    ("Kecskemet", 110000),
    ("Szekesfehervar", 97000),
    ("Szombathely", 78000),
]


def _format_cities_file(rows: list[tuple[str, int]]) -> str:
    return "\n".join(f"{name} {pop}" for name, pop in rows) + "\n"


def _task_count(rows: list[tuple[str, int]]) -> tuple[str, str, str]:
    title = "Városok száma"
    description = "Olvasd be a cities.txt fájlt, és írd ki a városok számát!"
    expected = str(len(rows))
    return title, description, expected


def _task_maximum(rows: list[tuple[str, int]], field: str = "population") -> tuple[str, str, str]:
    title = "Legnépesebb város"
    description = "Határozd meg a legnagyobb népességű város nevét, és írd ki!"
    best = max(rows, key=lambda r: r[1])
    expected = best[0]
    return title, description, expected


def _task_sum(rows: list[tuple[str, int]]) -> tuple[str, str, str]:
    title = "Össznépesség"
    description = "Számold ki a városok össznépességét, és írd ki!"
    expected = str(sum(r[1] for r in rows))
    return title, description, expected


TASK_BUILDERS = {
    "count": lambda rows, spec: _task_count(rows),
    "maximum": lambda rows, spec: _task_maximum(rows, spec.get("field", "population")),
    "sum": lambda rows, spec: _task_sum(rows),
}


def generate_dataset(template: dict[str, Any], rng: random.Random) -> list[tuple[str, int]]:
    dataset = template.get("dataset", {})
    dtype = dataset.get("type", "cities")
    if dtype != "cities":
        raise ValueError(f"Unsupported dataset type: {dtype}")

    count = dataset.get("count", rng.randint(3, 8))
    pool = list(DEFAULT_CITIES)
    rng.shuffle(pool)
    rows = pool[: min(count, len(pool))]
    # Slight population jitter so variants differ
    return [(name, max(1000, pop + rng.randint(-5000, 5000))) for name, pop in rows]


def build_story(template: dict[str, Any], rows: list[tuple[str, int]], use_ai: bool = False) -> str:
    default = (
        "Egy statisztikai hivatal a magyar városok népességét tartja nyilván. "
        f"A cities.txt fájl {len(rows)} város nevét és lakosságszámát tartalmazza "
        "(szóközzel elválasztva). Oldd meg a feladatokat a fájl alapján!"
    )
    if use_ai:
        return ai_generator.rewrite_story(default, context={"title": template.get("title", "Cities"), "rows": rows})
    return template.get("story") or default


def create_exam_from_template(
    db: Session,
    template: dict[str, Any],
    *,
    use_ai: bool = False,
    seed: int | None = None,
) -> Exam:
    rng = random.Random(seed)

    rows = generate_dataset(template, rng)
    if use_ai:
        rows = ai_generator.vary_dataset(rows, rng)

    story = build_story(template, rows, use_ai=use_ai)
    title = template.get("title", "Cities")
    description = template.get("description", "Adatfeldolgozás szöveges fájlból")

    exam = Exam(
        title=title,
        description=description,
        story=story,
        template_type=template.get("dataset", {}).get("type", "cities"),
    )
    db.add(exam)
    db.flush()

    dataset_content = _format_cities_file(rows)
    db.add(ExamFile(exam_id=exam.id, filename="cities.txt", content=dataset_content, read_only=True))
    db.add(ExamFile(exam_id=exam.id, filename="main.py", content="", read_only=False))

    for idx, task_spec in enumerate(template.get("tasks", [])):
        ttype = task_spec.get("type", "count")
        builder = TASK_BUILDERS.get(ttype)
        if not builder:
            raise ValueError(f"Unknown task type: {ttype}")
        title_t, desc, expected = builder(rows, task_spec)
        points = int(task_spec.get("points", 1))

        task = Task(
            exam_id=exam.id,
            title=title_t,
            description=desc,
            points=points,
            order_index=idx,
        )
        db.add(task)
        db.flush()

        # Visible sample test uses the main dataset
        db.add(
            TestCase(
                task_id=task.id,
                name=f"{ttype}-sample",
                input_files="{}",
                expected_output=expected,
                is_hidden=False,
                points=points,
            )
        )

        # Hidden variant with a smaller shuffled subset
        hidden_rows = rows[:]
        rng.shuffle(hidden_rows)
        hidden_rows = hidden_rows[: max(2, len(hidden_rows) - 1)]
        _, _, hidden_expected = builder(hidden_rows, task_spec)
        db.add(
            TestCase(
                task_id=task.id,
                name=f"{ttype}-hidden",
                input_files=json.dumps({"cities.txt": _format_cities_file(hidden_rows)}),
                expected_output=hidden_expected,
                is_hidden=True,
                points=points,
            )
        )

    db.commit()
    db.refresh(exam)
    return exam


SAMPLE_TEMPLATE: dict[str, Any] = {
    "title": "Cities",
    "description": "Olvasd be a cities.txt fájlt, és oldd meg a feladatokat!",
    "dataset": {
        "type": "cities",
        "fields": ["name", "population"],
        "count": 3,
    },
    "tasks": [
        {"type": "count", "points": 1},
        {"type": "maximum", "field": "population", "points": 2},
    ],
}
