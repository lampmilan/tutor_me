"""AI helpers for exam generation (Phase 8).

LLM may ONLY:
- rewrite story context
- generate realistic data variations

LLM must NOT decide grading logic — that comes from templates.
"""

from __future__ import annotations

import random
from typing import Any

from app.config import get_settings

settings = get_settings()


def rewrite_story(base_story: str, context: dict[str, Any] | None = None) -> str:
    """Rewrite the exam story. Falls back to base_story if AI is disabled."""
    if not settings.ai_generation_enabled or not settings.openai_api_key:
        return base_story

    try:
        import httpx

        prompt = (
            "You rewrite Hungarian programming érettségi exam stories. "
            "Keep the same factual requirements (file name, fields, task goals). "
            "Only change narrative flavor. Reply with the story text only.\n\n"
            f"Context: {context or {}}\n\n"
            f"Story:\n{base_story}"
        )
        resp = httpx.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {settings.openai_api_key}"},
            json={
                "model": settings.openai_model,
                "messages": [
                    {"role": "system", "content": "You help create Hungarian exam narratives."},
                    {"role": "user", "content": prompt},
                ],
                "temperature": 0.8,
            },
            timeout=30.0,
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"].strip()
    except Exception:
        return base_story


def vary_dataset(rows: list[tuple[str, int]], rng: random.Random) -> list[tuple[str, int]]:
    """Optionally ask the LLM for alternate city names; otherwise jitter locally."""
    if not settings.ai_generation_enabled or not settings.openai_api_key:
        return [(name, max(1000, pop + rng.randint(-3000, 3000))) for name, pop in rows]

    try:
        import httpx
        import json

        prompt = (
            "Generate a JSON array of Hungarian city objects with keys name and population. "
            f"Return exactly {len(rows)} cities. Populations should be realistic integers. "
            "Reply with JSON only."
        )
        resp = httpx.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {settings.openai_api_key}"},
            json={
                "model": settings.openai_model,
                "messages": [
                    {"role": "system", "content": "Return valid JSON only."},
                    {"role": "user", "content": prompt},
                ],
                "temperature": 0.9,
            },
            timeout=30.0,
        )
        resp.raise_for_status()
        text = resp.json()["choices"][0]["message"]["content"].strip()
        if text.startswith("```"):
            text = text.strip("`")
            if text.startswith("json"):
                text = text[4:].strip()
        data = json.loads(text)
        parsed = [(item["name"], int(item["population"])) for item in data]
        if len(parsed) == len(rows):
            return parsed
    except Exception:
        pass

    return [(name, max(1000, pop + rng.randint(-3000, 3000))) for name, pop in rows]
