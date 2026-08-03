from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Exam(Base):
    __tablename__ = "exams"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, default="")
    story: Mapped[str] = mapped_column(Text, default="")
    template_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    files: Mapped[list["ExamFile"]] = relationship(back_populates="exam", cascade="all, delete-orphan")
    tasks: Mapped[list["Task"]] = relationship(back_populates="exam", cascade="all, delete-orphan")
    workspaces: Mapped[list["Workspace"]] = relationship(back_populates="exam", cascade="all, delete-orphan")


class ExamFile(Base):
    """Template files that ship with an exam (copied into workspaces)."""

    __tablename__ = "exam_files"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    exam_id: Mapped[int] = mapped_column(ForeignKey("exams.id", ondelete="CASCADE"), index=True)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, default="")
    read_only: Mapped[bool] = mapped_column(default=False)

    exam: Mapped["Exam"] = relationship(back_populates="files")


class Workspace(Base):
    __tablename__ = "workspaces"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    exam_id: Mapped[int] = mapped_column(ForeignKey("exams.id", ondelete="CASCADE"), index=True)
    user_id: Mapped[str] = mapped_column(String(100), default="anonymous", index=True)
    path: Mapped[str] = mapped_column(String(512), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    exam: Mapped["Exam"] = relationship(back_populates="workspaces")
    files: Mapped[list["File"]] = relationship(back_populates="workspace", cascade="all, delete-orphan")


class File(Base):
    __tablename__ = "files"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    workspace_id: Mapped[int] = mapped_column(ForeignKey("workspaces.id", ondelete="CASCADE"), index=True)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, default="")
    read_only: Mapped[bool] = mapped_column(default=False)

    workspace: Mapped["Workspace"] = relationship(back_populates="files")


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    exam_id: Mapped[int] = mapped_column(ForeignKey("exams.id", ondelete="CASCADE"), index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, default="")
    points: Mapped[int] = mapped_column(Integer, default=1)
    order_index: Mapped[int] = mapped_column(Integer, default=0)
    # JSON list of educational hints shown when hidden tests fail
    hints_json: Mapped[str] = mapped_column(Text, default="[]")
    # Python file students edit/run for this phase (e.g. varosok_szama.py)
    solution_file: Mapped[str] = mapped_column(String(255), default="main.py")

    exam: Mapped["Exam"] = relationship(back_populates="tasks")
    test_cases: Mapped[list["TestCase"]] = relationship(back_populates="task", cascade="all, delete-orphan")


class TestCase(Base):
    __tablename__ = "test_cases"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id", ondelete="CASCADE"), index=True)
    name: Mapped[str] = mapped_column(String(255), default="test")
    # Optional stdin or replacement input files as JSON map: {"cities.txt": "A 1\nB 2"}
    input_files: Mapped[str] = mapped_column(Text, default="{}")
    stdin: Mapped[str] = mapped_column(Text, default="")
    expected_output: Mapped[str] = mapped_column(Text, default="")
    is_hidden: Mapped[bool] = mapped_column(default=True)
    points: Mapped[int] = mapped_column(Integer, default=1)

    task: Mapped["Task"] = relationship(back_populates="test_cases")


class Submission(Base):
    __tablename__ = "submissions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    workspace_id: Mapped[int] = mapped_column(ForeignKey("workspaces.id", ondelete="CASCADE"), index=True)
    task_id: Mapped[int | None] = mapped_column(ForeignKey("tasks.id", ondelete="SET NULL"), nullable=True)
    points_earned: Mapped[float] = mapped_column(Float, default=0)
    points_possible: Mapped[float] = mapped_column(Float, default=0)
    result_json: Mapped[str] = mapped_column(Text, default="{}")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
