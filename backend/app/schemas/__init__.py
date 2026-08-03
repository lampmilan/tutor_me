from datetime import datetime

from pydantic import BaseModel, model_validator


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
    is_hidden: bool
    points: int

    model_config = {"from_attributes": True}

    @model_validator(mode="after")
    def redact_hidden(self) -> "TestCaseOut":
        if self.is_hidden:
            self.expected_output = None
        return self



class TaskOut(BaseModel):
    id: int
    title: str
    description: str
    points: int
    order_index: int
    uses_preamble: bool = False
    starter: str = ""
    entry_filename: str = "main.py"
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
    created_at: datetime
    files: list[ExamFileOut] = []
    tasks: list[TaskOut] = []

    model_config = {"from_attributes": True}


class ExamListItem(BaseModel):
    id: int
    title: str
    description: str
    created_at: datetime

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


class TestResult(BaseModel):
    test_case_id: int
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
