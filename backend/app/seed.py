"""Seed the Cities example exam used for end-to-end development."""

from sqlalchemy.orm import Session

from app.models import Exam, ExamFile, Task, TestCase


CITIES_CONTENT = """Budapest 1780000
Szeged 160000
Pecs 140000
"""


def seed_cities_exam(db: Session) -> Exam:
    existing = db.query(Exam).filter(Exam.title == "Cities").first()
    if existing:
        return existing

    exam = Exam(
        title="Cities",
        description="Olvasd be a cities.txt fájlt, és oldd meg a feladatokat!",
        story=(
            "Egy statisztikai hivatal a magyar városok népességét tartja nyilván. "
            "A cities.txt fájl három város nevét és lakosságszámát tartalmazza "
            "(szóközzel elválasztva). Oldd meg a feladatokat a fájl alapján!"
        ),
        template_type="cities",
    )
    db.add(exam)
    db.flush()

    db.add(ExamFile(exam_id=exam.id, filename="cities.txt", content=CITIES_CONTENT, read_only=True))
    db.add(ExamFile(exam_id=exam.id, filename="main.py", content="", read_only=False))

    task1 = Task(
        exam_id=exam.id,
        title="Városok száma",
        description="Olvasd be a cities.txt fájlt, és írd ki a városok számát!",
        points=1,
        order_index=0,
    )
    db.add(task1)
    db.flush()
    db.add(
        TestCase(
            task_id=task1.id,
            name="count-sample",
            input_files="{}",
            expected_output="3",
            is_hidden=False,
            points=1,
        )
    )
    db.add(
        TestCase(
            task_id=task1.id,
            name="count-hidden",
            input_files='{"cities.txt": "A 10\\nB 20\\nC 30\\nD 40\\n"}',
            expected_output="4",
            is_hidden=True,
            points=1,
        )
    )

    task2 = Task(
        exam_id=exam.id,
        title="Legnépesebb város",
        description="Határozd meg a legnagyobb népességű város nevét, és írd ki!",
        points=2,
        order_index=1,
    )
    db.add(task2)
    db.flush()
    db.add(
        TestCase(
            task_id=task2.id,
            name="max-sample",
            input_files="{}",
            expected_output="Budapest",
            is_hidden=False,
            points=2,
        )
    )
    db.add(
        TestCase(
            task_id=task2.id,
            name="max-hidden",
            input_files='{"cities.txt": "Alpha 100\\nBeta 500\\nGamma 200\\n"}',
            expected_output="Beta",
            is_hidden=True,
            points=2,
        )
    )

    db.commit()
    db.refresh(exam)
    return exam
