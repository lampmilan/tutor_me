from pydantic import BaseModel, Field


class TaskTemplate(BaseModel):
    type: str
    title: str
    description: str = ""
    points: int = 1
    field: str | None = None
    label_field: str | None = None
    op: str | None = None
    value: str | int | float | None = None
    hints: list[str] = Field(default_factory=list)


class ExamTemplate(BaseModel):
    id: str
    title: str
    description: str = ""
    story: str = ""
    data_file: str
    dataset_type: str
    visible: str
    hidden: list[str] = Field(default_factory=list)
    tasks: list[TaskTemplate] = Field(default_factory=list)


class TemplateGenerateBody(BaseModel):
    """Generate/materialize an exam from a catalog id or inline template."""

    exam_id: str | None = None
    template: dict | None = None
    use_ai: bool = False
    seed: int | None = None
