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
