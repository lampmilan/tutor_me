"""Oracle for Szólánc — students never see this module.

The exam is fully interactive: answers come from stdin, not the data file.
"""

from __future__ import annotations

from typing import Any, Callable

from app.exams.builders import Row

LENGTH_ERROR = "A karakterek száma téves!"
MATCH_ERROR = "Nem illeszkedett!"


def parse_szolanc(content: str) -> list[Row]:
    # Placeholder file — the word chain lives on stdin.
    return [{"index": 1, "raw": content, "n": 0}]


def parse(content: str) -> list[Row]:
    return parse_szolanc(content)


def _words_from_spec(spec: dict[str, Any]) -> list[str]:
    raw = str(spec.get("stdin") or "")
    return [line.strip() for line in raw.splitlines() if line.strip()]


def _play(words: list[str]) -> tuple[list[str], str | None, int]:
    """Return (prompt lines, stop reason, number of legal words before the error)."""
    prompts: list[str] = []
    valid: list[str] = []
    reason: str | None = None
    for i, word in enumerate(words):
        prompts.append(f"{i + 1}. szó:")
        if i == 0:
            valid.append(word)
            continue
        prev = valid[-1]
        if len(word) != 6:
            reason = LENGTH_ERROR
            break
        if word[0] != prev[-1]:
            reason = MATCH_ERROR
            break
        valid.append(word)
    return prompts, reason, len(valid)


def _level(steps: int) -> str:
    if steps <= 2:
        return "kezdő"
    if steps <= 5:
        return "közepes"
    return "haladó"


def _full_output(spec: dict[str, Any]) -> str:
    prompts, reason, steps = _play(_words_from_spec(spec))
    lines = list(prompts)
    if reason:
        lines.append(reason)
    lines.append(f"Helyes lépések száma: {steps}")
    lines.append(f"Szint: {_level(steps)}")
    return "\n".join(lines)


def _task_szolanc_teljes(_rows: list[Row], spec: dict[str, Any]) -> str:
    return _full_output(spec)


TASK_BUILDERS: dict[str, Callable[[list[Row], dict[str, Any]], str]] = {
    "szolanc_teljes": _task_szolanc_teljes,
}
