"""Exam catalog loader: folders under app/exams/<id>/."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from app.schemas.templates import ExamTemplate

EXAMS_ROOT = Path(__file__).resolve().parent


@dataclass
class LoadedExam:
    template: ExamTemplate
    root: Path
    visible_content: str
    hidden_contents: list[str]


def list_exam_dirs() -> list[Path]:
    if not EXAMS_ROOT.is_dir():
        return []
    dirs = []
    for path in sorted(EXAMS_ROOT.iterdir()):
        if path.is_dir() and (path / "template.json").is_file():
            dirs.append(path)
    return dirs


def load_exam_dir(exam_dir: Path) -> LoadedExam:
    raw = json.loads((exam_dir / "template.json").read_text(encoding="utf-8"))
    template = ExamTemplate.model_validate(raw)

    visible_path = exam_dir / template.visible
    if not visible_path.is_file():
        raise FileNotFoundError(f"Visible dataset missing: {visible_path}")
    visible_content = visible_path.read_text(encoding="utf-8")
    if not visible_content.endswith("\n") and visible_content:
        visible_content += "\n"

    hidden_contents: list[str] = []
    for rel in template.hidden:
        hidden_path = exam_dir / rel
        if not hidden_path.is_file():
            raise FileNotFoundError(f"Hidden dataset missing: {hidden_path}")
        content = hidden_path.read_text(encoding="utf-8")
        if not content.endswith("\n") and content:
            content += "\n"
        hidden_contents.append(content)

    return LoadedExam(
        template=template,
        root=exam_dir,
        visible_content=visible_content,
        hidden_contents=hidden_contents,
    )


def load_exam_by_id(exam_id: str) -> LoadedExam:
    exam_dir = EXAMS_ROOT / exam_id
    if not (exam_dir / "template.json").is_file():
        raise FileNotFoundError(f"Unknown exam id: {exam_id}")
    return load_exam_dir(exam_dir)


def discover_exams() -> list[LoadedExam]:
    return [load_exam_dir(path) for path in list_exam_dirs()]
