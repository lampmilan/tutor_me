from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, field_validator, model_validator


class ExamFileOut(BaseModel):
    id: int
    filename: str
    content: str
    read_only: bool

    model_config = {"from_attributes": True}


class TestCaseOut(BaseModel):
    id: int
    name: str
    expected_output: str | None = None
    stdin: str = ""
    is_hidden: bool
    points: int

    model_config = {"from_attributes": True}

    @model_validator(mode="after")
    def redact_hidden(self) -> "TestCaseOut":
        if self.is_hidden:
            self.expected_output = None
            self.stdin = ""
        return self



class TaskOut(BaseModel):
    id: int
    title: str
    description: str
    points: int
    order_index: int
    solution_file: str = "main.py"
    uses_preamble: bool = False
    starter: str = ""
    tags: list[str] = []
    stdin: str = ""
    expected_file: str = ""
    test_cases: list[TestCaseOut] = []

    model_config = {"from_attributes": True}


class ExamOut(BaseModel):
    id: int
    title: str
    description: str
    story: str
    template_type: str | None
    preamble: str = ""
    shared_variable: str = "data"
    level: str = "kozep"
    difficulty: int = 2
    tags: list[str] = []
    constraints: list[str] = []
    data_explanation: str = ""
    created_at: datetime
    files: list[ExamFileOut] = []
    tasks: list[TaskOut] = []

    model_config = {"from_attributes": True}


class ExamListItem(BaseModel):
    id: int
    title: str
    description: str
    created_at: datetime
    level: str = "kozep"
    difficulty: int = 2
    tags: list[str] = []

    model_config = {"from_attributes": True}


class FileOut(BaseModel):
    id: int
    filename: str
    content: str
    read_only: bool

    model_config = {"from_attributes": True}


class FileUpdate(BaseModel):
    content: str


class WorkspaceOut(BaseModel):
    id: int
    exam_id: int
    user_id: str
    path: str
    files: list[FileOut] = []

    model_config = {"from_attributes": True}


class StartExamRequest(BaseModel):
    user_id: str = "anonymous"


class ExecuteRequest(BaseModel):
    workspace_id: int
    task_id: int | None = None
    # Optional: save this as the active feladat source before running
    code: str | None = None
    filename: str | None = None  # optional; used to resolve task if task_id omitted
    stdin: str = ""


class ExecuteResponse(BaseModel):
    output: str = ""
    error: str = ""
    runtime: float = 0.0
    exit_code: int = 0


class JudgeRequest(BaseModel):
    workspace_id: int
    task_id: int | None = None  # None = all tasks
    code: str | None = None
    filename: str | None = None  # optional file to save code into before judging


class TestResult(BaseModel):
    test_case_id: int
    task_id: int | None = None
    name: str
    label: str = ""
    passed: bool
    points_earned: int
    points_possible: int
    expected: str | None = None
    actual: str | None = None
    error: str = ""
    runtime: float = 0.0
    is_hidden: bool = True


class JudgeResponse(BaseModel):
    points_earned: float
    points_possible: float
    passed_count: int = 0
    total_count: int = 0
    summary_line: str = ""
    failed_labels: list[str] = []
    hints: list[str] = []
    results: list[TestResult]


class GenerateExamResponse(BaseModel):
    exam: ExamOut


FEEDBACK_MESSAGE_MAX = 4000
PRODUCT_PAY_OPTIONS = ("guides", "more_exams", "videos", "nothing")


class FeedbackIn(BaseModel):
    feedback_type: Literal["problem", "idea", "product"]
    exam_title: str | None = None
    task_title: str | None = None
    message: str = Field(default="", max_length=FEEDBACK_MESSAGE_MAX)
    rating: int | None = None
    would_pay_for: list[str] | None = None

    @field_validator("exam_title", "task_title", mode="before")
    @classmethod
    def blank_title_to_none(cls, value: object) -> str | None:
        if value is None:
            return None
        text = str(value).strip()
        return text[:255] if text else None

    @field_validator("message", mode="before")
    @classmethod
    def strip_message(cls, value: object) -> str:
        if value is None:
            return ""
        return str(value).strip()

    @model_validator(mode="after")
    def validate_by_type(self) -> "FeedbackIn":
        if self.feedback_type in ("problem", "idea"):
            if not self.message:
                raise ValueError("message required")
            self.rating = None
            self.would_pay_for = None
            return self
        if self.rating is None or self.rating < 1 or self.rating > 5:
            raise ValueError("rating must be 1-5")
        opts = list(dict.fromkeys(self.would_pay_for or []))
        allowed = set(PRODUCT_PAY_OPTIONS)
        if not opts:
            raise ValueError("would_pay_for required")
        if any(item not in allowed for item in opts):
            raise ValueError("invalid would_pay_for")
        if "nothing" in opts and opts != ["nothing"]:
            raise ValueError("nothing is exclusive")
        self.would_pay_for = opts
        return self


class FeedbackOut(BaseModel):
    id: int
    feedback_type: str
    exam_title: str
    task_title: str
    message: str
    rating: int | None = None
    would_pay_for: list[str] = Field(default_factory=list)
    created_at: datetime

    model_config = {"from_attributes": True}


class FeedbackCreated(BaseModel):
    id: int
