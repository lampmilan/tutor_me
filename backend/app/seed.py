"""Seed the Cities example exam used for end-to-end development."""

from __future__ import annotations

import json

from sqlalchemy.orm import Session, joinedload

from app.models import Exam, ExamFile, Task, TestCase


CITIES_CONTENT = """Budapest 1780000
Szeged 160000
Pecs 140000
"""

HIDDEN_READ = "A 10\nB 20\nC 30\nD 40\n"
HIDDEN_COUNT = HIDDEN_READ
HIDDEN_MAX = "Alpha 100\nBeta 500\nGamma 200\n"

# Marker used to detect whether an existing seed needs a content refresh
STORY_VERSION_MARKER = "[[cities-v2]]"

CITIES_STORY = f"""{STORY_VERSION_MARKER}
Egy statisztikai hivatal a magyar városok népességét tartja nyilván. A hivatal
munkatársai a települések adatait szöveges fájlban gyűjtik, majd programokkal
értékelik ki. Ebben a feladatban Önnek kell feldolgoznia a cities.txt fájlban
tárolt városadatokat!

A cities.txt fájl minden sora egy város adatait tartalmazza. A sorban először
a város neve, majd szóközzel elválasztva a lakosságszám (egész szám) szerepel:

Városnév Lakosságszám

Az alábbi táblázat mutatja a fájl mezőinek jelentését:

Mező          Jelentés
Városnév      A település neve (ékezet nélküli írásmód is előfordulhat)
Lakosságszám  A település lakóinak száma főben

Az alábbi példa a cities.txt fájl tartalmát mutatja:

Budapest 1780000
Szeged 160000
Pecs 140000

Ebben a példában három város szerepel. Budapest a legnépesebb település
1 780 000 fővel, Szeged 160 000, Pécs pedig 140 000 fővel rendelkezik.

Készítsen programot, amely kiértékeli a cities.txt fájl tartalmát! A megoldást
fázisonként, külön Python fájlokban készítse el (beolvasas.py, varosok_szama.py,
nepesseg.py). A program megírásakor a fájl adatainak helyességét, érvényességét
nem kell ellenőriznie, és feltételezheti, hogy a rendelkezésre álló adatok
a leírtaknak megfelelnek.

A képernyőre írást igénylő részfeladatok esetén az ékezetmentes kiírás is
elfogadott. A mintához tartalmában hasonlóan jelenítse meg az eredményt!
"""

CITIES_DESCRIPTION = (
    "Értékelje ki a cities.txt fájlban tárolt városok népességadatait!"
)


def _replace_exam_files(db: Session, exam: Exam, files: list[tuple[str, str, bool]]) -> None:
    for existing in list(exam.files):
        db.delete(existing)
    db.flush()
    for filename, content, read_only in files:
        db.add(
            ExamFile(
                exam_id=exam.id,
                filename=filename,
                content=content,
                read_only=read_only,
            )
        )


def _replace_tasks(db: Session, exam: Exam, tasks: list[dict]) -> None:
    for existing in list(exam.tasks):
        db.delete(existing)
    db.flush()
    for spec in tasks:
        task = Task(
            exam_id=exam.id,
            title=spec["title"],
            description=spec["description"],
            points=spec["points"],
            order_index=spec["order_index"],
            solution_file=spec["solution_file"],
        )
        db.add(task)
        db.flush()
        for tc in spec["test_cases"]:
            db.add(
                TestCase(
                    task_id=task.id,
                    name=tc["name"],
                    input_files=tc["input_files"],
                    expected_output=tc["expected_output"],
                    is_hidden=tc["is_hidden"],
                    points=tc["points"],
                )
            )


def _cities_phase_specs() -> list[dict]:
    return [
        {
            "title": "Beolvasás",
            "description": (
                "Olvassa be a cities.txt fájlt, és írja ki a fájl teljes tartalmát "
                "a képernyőre! Feltételezheti, hogy a fájl létezik, és a sorok "
                "a leírt formátumot követik. A kiírás legyen soronként azonos "
                "a fájl tartalmával (városnév, szóköz, lakosságszám)."
            ),
            "points": 1,
            "order_index": 0,
            "solution_file": "beolvasas.py",
            "test_cases": [
                {
                    "name": "read-sample",
                    "input_files": "{}",
                    "expected_output": CITIES_CONTENT.rstrip("\n"),
                    "is_hidden": False,
                    "points": 1,
                },
                {
                    "name": "read-hidden",
                    "input_files": json.dumps({"cities.txt": HIDDEN_READ}),
                    "expected_output": HIDDEN_READ.rstrip("\n"),
                    "is_hidden": True,
                    "points": 1,
                },
            ],
        },
        {
            "title": "Városok száma",
            "description": (
                "Számítsa ki és a mintának megfelelően jelenítse meg a fájlban "
                "szereplő városok számát! A program csak a városok darabszámát "
                "írja a képernyőre (egy egész számot)."
            ),
            "points": 1,
            "order_index": 1,
            "solution_file": "varosok_szama.py",
            "test_cases": [
                {
                    "name": "count-sample",
                    "input_files": "{}",
                    "expected_output": "3",
                    "is_hidden": False,
                    "points": 1,
                },
                {
                    "name": "count-hidden",
                    "input_files": json.dumps({"cities.txt": HIDDEN_COUNT}),
                    "expected_output": "4",
                    "is_hidden": True,
                    "points": 1,
                },
            ],
        },
        {
            "title": "Legnépesebb város",
            "description": (
                "Határozza meg a legnagyobb népességű város nevét, és írja ki "
                "a képernyőre! Ha több városnak is azonos a legnagyobb "
                "lakosságszáma, bármelyik megfelelő nevét kiírhatja. "
                "A kimenet csak a város neve legyen."
            ),
            "points": 2,
            "order_index": 2,
            "solution_file": "nepesseg.py",
            "test_cases": [
                {
                    "name": "max-sample",
                    "input_files": "{}",
                    "expected_output": "Budapest",
                    "is_hidden": False,
                    "points": 2,
                },
                {
                    "name": "max-hidden",
                    "input_files": json.dumps({"cities.txt": HIDDEN_MAX}),
                    "expected_output": "Beta",
                    "is_hidden": True,
                    "points": 2,
                },
            ],
        },
    ]


def _cities_files() -> list[tuple[str, str, bool]]:
    return [
        ("cities.txt", CITIES_CONTENT, True),
        ("beolvasas.py", "", False),
        ("varosok_szama.py", "", False),
        ("nepesseg.py", "", False),
    ]


def _needs_cities_upgrade(exam: Exam) -> bool:
    if STORY_VERSION_MARKER not in (exam.story or ""):
        return True
    filenames = {f.filename for f in exam.files}
    expected = {"cities.txt", "beolvasas.py", "varosok_szama.py", "nepesseg.py"}
    if filenames != expected:
        return True
    if len(exam.tasks) != 3:
        return True
    by_order = sorted(exam.tasks, key=lambda t: t.order_index)
    expected_files = ["beolvasas.py", "varosok_szama.py", "nepesseg.py"]
    for task, solution in zip(by_order, expected_files):
        if getattr(task, "solution_file", None) != solution:
            return True
    return False


def seed_cities_exam(db: Session) -> Exam:
    existing = (
        db.query(Exam)
        .options(joinedload(Exam.files), joinedload(Exam.tasks))
        .filter(Exam.title == "Cities")
        .first()
    )

    story = CITIES_STORY
    description = CITIES_DESCRIPTION

    if existing and not _needs_cities_upgrade(existing):
        return existing

    if existing:
        exam = existing
        exam.description = description
        exam.story = story
        exam.template_type = "cities"
        _replace_exam_files(db, exam, _cities_files())
        _replace_tasks(db, exam, _cities_phase_specs())
        db.commit()
        db.refresh(exam)
        return exam

    exam = Exam(
        title="Cities",
        description=description,
        story=story,
        template_type="cities",
    )
    db.add(exam)
    db.flush()

    for filename, content, read_only in _cities_files():
        db.add(
            ExamFile(
                exam_id=exam.id,
                filename=filename,
                content=content,
                read_only=read_only,
            )
        )

    for spec in _cities_phase_specs():
        task = Task(
            exam_id=exam.id,
            title=spec["title"],
            description=spec["description"],
            points=spec["points"],
            order_index=spec["order_index"],
            solution_file=spec["solution_file"],
        )
        db.add(task)
        db.flush()
        for tc in spec["test_cases"]:
            db.add(
                TestCase(
                    task_id=task.id,
                    name=tc["name"],
                    input_files=tc["input_files"],
                    expected_output=tc["expected_output"],
                    is_hidden=tc["is_hidden"],
                    points=tc["points"],
                )
            )

    db.commit()
    db.refresh(exam)
    return exam
