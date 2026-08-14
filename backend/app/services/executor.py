"""Isolated code execution service.

Primary backend: Docker (CPU/memory/time/network limits).
Fallback: subprocess (for local Compose when Docker CLI is unavailable).
"""

from __future__ import annotations

import resource
import shutil
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass, field
from pathlib import Path

from app.config import get_settings

settings = get_settings()


@dataclass
class ExecutionResult:
    output: str
    error: str
    runtime: float
    exit_code: int
    files: dict[str, str] = field(default_factory=dict)


def execute_python(
    workspace_path: str | Path,
    *,
    entrypoint: str = "main.py",
    stdin: str = "",
    timeout: int | None = None,
    extra_files: dict[str, str] | None = None,
    capture_files: list[str] | None = None,
    isolate: bool = False,
) -> ExecutionResult:
    """Run a Python entrypoint inside an isolated environment.

    If extra_files is provided, a temporary copy of the workspace is used
    so test input files do not mutate the student's workspace.
    """
    timeout = timeout or settings.execution_timeout_seconds
    src = Path(workspace_path)
    script = entrypoint or "main.py"
    capture = [name for name in (capture_files or []) if name]
    needs_copy = isolate or extra_files is not None or bool(capture)

    if needs_copy:
        with tempfile.TemporaryDirectory(prefix="exec-") as tmp:
            tmp_path = Path(tmp)
            for item in src.iterdir():
                dest = tmp_path / item.name
                if item.is_file():
                    shutil.copy2(item, dest)
                elif item.is_dir():
                    shutil.copytree(item, dest)
            if extra_files:
                for name, content in extra_files.items():
                    (tmp_path / name).write_text(content, encoding="utf-8")
            result = _run(tmp_path, entrypoint=script, stdin=stdin, timeout=timeout)
            for name in capture:
                path = tmp_path / name
                if path.is_file():
                    result.files[name] = path.read_text(encoding="utf-8")
            return result

    return _run(src, entrypoint=script, stdin=stdin, timeout=timeout)


def _run(
    workspace_path: Path,
    *,
    entrypoint: str,
    stdin: str,
    timeout: int,
) -> ExecutionResult:
    backend = settings.execution_backend.lower()
    if backend == "docker" and shutil.which("docker"):
        return _run_docker(workspace_path, entrypoint=entrypoint, stdin=stdin, timeout=timeout)
    return _run_subprocess(workspace_path, entrypoint=entrypoint, stdin=stdin, timeout=timeout)


def _run_docker(
    workspace_path: Path,
    *,
    entrypoint: str,
    stdin: str,
    timeout: int,
) -> ExecutionResult:
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
        f"{host_path}:/workspace:rw",
        "-w",
        "/workspace",
        settings.executor_image,
        "python",
        entrypoint,
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
        return _run_subprocess(workspace_path, entrypoint=entrypoint, stdin=stdin, timeout=timeout)


def _python_bin() -> str:
    """Interpreter used for subprocess execution (backend container's Python)."""
    return sys.executable or "/usr/local/bin/python3"


def _memory_limit_bytes() -> int:
    raw = (settings.execution_memory_limit or "128m").strip().lower()
    try:
        if raw.endswith("g"):
            return int(float(raw[:-1]) * 1024 * 1024 * 1024)
        if raw.endswith("m"):
            return int(float(raw[:-1]) * 1024 * 1024)
        if raw.endswith("k"):
            return int(float(raw[:-1]) * 1024)
        return int(raw)
    except ValueError:
        return 128 * 1024 * 1024


def _limit_child_resources() -> None:
    """Apply CPU/address-space caps in the forked student process (Cloud Run)."""
    cpu = max(1, int(settings.execution_timeout_seconds) + 1)
    mem = _memory_limit_bytes()
    try:
        resource.setrlimit(resource.RLIMIT_CPU, (cpu, cpu))
    except (ValueError, resource.error):
        pass
    try:
        resource.setrlimit(resource.RLIMIT_AS, (mem, mem))
    except (ValueError, resource.error):
        pass


def _run_subprocess(
    workspace_path: Path,
    *,
    entrypoint: str,
    stdin: str,
    timeout: int,
) -> ExecutionResult:
    """Run student code via subprocess (Compose / Cloud Run)."""
    started = time.perf_counter()
    python_bin = _python_bin()
    script = entrypoint or "main.py"
    try:
        proc = subprocess.run(
            [python_bin, script],
            cwd=str(workspace_path),
            input=stdin,
            capture_output=True,
            text=True,
            timeout=timeout,
            start_new_session=True,
            preexec_fn=_limit_child_resources,
            env={
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
