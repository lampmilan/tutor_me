from typing import Literal

from pydantic import BaseModel, Field


class AuxFileTemplate(BaseModel):
    filename: str
    content: str
    read_only: bool = True


class TaskTemplate(BaseModel):
    type: str
    title: str
    description: str = ""
    points: int = 1
    field: str | None = None
    label_field: str | None = None
    op: str | None = None
    # Used by count_where (threshold) and literal (authored expected output)
    value: str | int | float | None = None
    solution_file: str | None = None
    hints: list[str] = Field(default_factory=list)
    # Option A: later tasks get a canonical load preamble injected at run time
    uses_preamble: bool = False
    # Monaco scaffold shown for this feladat (comments + stub)
    starter: str = ""
    tags: list[str] = Field(default_factory=list)
    stdin: str = ""
    # Per-hidden-dataset stdin overrides (aligned with exam hidden[] order)
    hidden_stdin: list[str] = Field(default_factory=list)
    expected_file: str = ""


class ExamTemplate(BaseModel):
    id: str
    title: str
    # False = keep the catalog folder (oracles/tests) but omit from GET /exams
    listed: bool = True
    description: str = ""
    story: str = ""
    data_file: str
    dataset_type: str
    visible: str
    hidden: list[str] = Field(default_factory=list)
    # Canonical loader injected before student code when uses_preamble=True
    shared_variable: str = "data"
    preamble: str = ""
    # Named function bodies appended after the file-load preamble ([function] tasks)
    functions: str = ""
    # Optional random seed injected at the start of the preamble ([random] tasks)
    seed: int | None = None
    aux_files: list[AuxFileTemplate] = Field(default_factory=list)
    level: str = "kozep"
    # official = real OH paper; synthetic = generated practice exam
    origin: Literal["official", "synthetic"] = "synthetic"
    difficulty: int = 2
    tags: list[str] = Field(default_factory=list)
    constraints: list[str] = Field(default_factory=list)
    data_explanation: str = ""
    tasks: list[TaskTemplate] = Field(default_factory=list)


class TemplateGenerateBody(BaseModel):
    """Generate/materialize an exam from a catalog id or inline template."""

    exam_id: str | None = None
    template: dict | None = None
    use_ai: bool = False
    seed: int | None = None
