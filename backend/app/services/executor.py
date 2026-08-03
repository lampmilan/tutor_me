"""Isolated code execution service.

Primary backend: Docker (CPU/memory/time/network limits).
Fallback: subprocess (for local Compose when Docker CLI is unavailable).
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path

from app.config import get_settings

settings = get_settings()


@dataclass
class ExecutionResult:
    output: str
    error: str
    runtime: float
    exit_code: int


def execute_python(
    workspace_path: str | Path,
    *,
    stdin: str = "",
    timeout: int | None = None,
    extra_files: dict[str, str] | None = None,
) -> ExecutionResult:
    """Run main.py inside an isolated environment.

    If extra_files is provided, a temporary copy of the workspace is used
    so test input files do not mutate the student's workspace.
    """
    timeout = timeout or settings.execution_timeout_seconds
    src = Path(workspace_path)

    if extra_files:
        with tempfile.TemporaryDirectory(prefix="exec-") as tmp:
            tmp_path = Path(tmp)
            for item in src.iterdir():
                dest = tmp_path / item.name
                if item.is_file():
                    shutil.copy2(item, dest)
                elif item.is_dir():
                    shutil.copytree(item, dest)
            for name, content in extra_files.items():
                (tmp_path / name).write_text(content, encoding="utf-8")
            return _run(tmp_path, stdin=stdin, timeout=timeout)

    return _run(src, stdin=stdin, timeout=timeout)


def _run(workspace_path: Path, *, stdin: str, timeout: int) -> ExecutionResult:
    backend = settings.execution_backend.lower()
    if backend == "docker" and shutil.which("docker"):
        return _run_docker(workspace_path, stdin=stdin, timeout=timeout)
    return _run_subprocess(workspace_path, stdin=stdin, timeout=timeout)


def _run_docker(workspace_path: Path, *, stdin: str, timeout: int) -> ExecutionResult:
    """Create a temporary container, mount workspace, run, destroy."""
    host_path = str(workspace_path.resolve())
    cmd = [
        "docker",
        "run",
        "--rm",
        "--network",
        "none",
        "--memory",
        settings.execution_memory_limit,
        "--cpus",
        settings.execution_cpu_limit,
        "--pids-limit",
        "64",
        "--read-only",
        "--tmpfs",
        "/tmp:rw,size=16m",
        "-v",
        f"{host_path}:/workspace:ro",
        "-w",
        "/workspace",
        settings.executor_image,
        "python",
        "main.py",
    ]

    started = time.perf_counter()
    try:
        proc = subprocess.run(
            cmd,
            input=stdin,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        runtime = time.perf_counter() - started
        return ExecutionResult(
            output=proc.stdout,
            error=proc.stderr,
            runtime=round(runtime, 4),
            exit_code=proc.returncode,
        )
    except subprocess.TimeoutExpired as exc:
        runtime = time.perf_counter() - started
        stdout = exc.stdout if isinstance(exc.stdout, str) else (exc.stdout or b"").decode(errors="replace")
        stderr = exc.stderr if isinstance(exc.stderr, str) else (exc.stderr or b"").decode(errors="replace")
        return ExecutionResult(
            output=stdout,
            error=(stderr + "\nExecution timed out.").strip(),
            runtime=round(runtime, 4),
            exit_code=124,
        )
    except FileNotFoundError:
        return _run_subprocess(workspace_path, stdin=stdin, timeout=timeout)


def _python_bin() -> str:
    """Interpreter used for subprocess execution (backend container's Python)."""
    return sys.executable or "/usr/local/bin/python3"


def _run_subprocess(workspace_path: Path, *, stdin: str, timeout: int) -> ExecutionResult:
    """Run student code in-process host via subprocess (Compose-friendly fallback)."""
    started = time.perf_counter()
    python_bin = _python_bin()
    try:
        proc = subprocess.run(
            [python_bin, "main.py"],
            cwd=str(workspace_path),
            input=stdin,
            capture_output=True,
            text=True,
            timeout=timeout,
            env={
                # Include /usr/local/bin — official Python images install there
                "PATH": "/usr/local/bin:/usr/bin:/bin",
                "HOME": "/tmp",
                "PYTHONDONTWRITEBYTECODE": "1",
            },
        )
        runtime = time.perf_counter() - started
        return ExecutionResult(
            output=proc.stdout,
            error=proc.stderr,
            runtime=round(runtime, 4),
            exit_code=proc.returncode,
        )
    except subprocess.TimeoutExpired as exc:
        runtime = time.perf_counter() - started
        stdout = exc.stdout if isinstance(exc.stdout, str) else (exc.stdout or b"").decode(errors="replace")
        stderr = exc.stderr if isinstance(exc.stderr, str) else (exc.stderr or b"").decode(errors="replace")
        return ExecutionResult(
            output=stdout,
            error=(stderr + "\nExecution timed out.").strip(),
            runtime=round(runtime, 4),
            exit_code=124,
        )
    except FileNotFoundError:
        runtime = time.perf_counter() - started
        return ExecutionResult(
            output="",
            error=f"Python interpreter not found: {python_bin}",
            runtime=round(runtime, 4),
            exit_code=127,
        )
