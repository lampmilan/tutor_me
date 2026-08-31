"""In-process sliding-window rate limiter for /execute and /judge."""

from __future__ import annotations

import threading
import time
from collections import deque

from fastapi import HTTPException, Request

from app.config import get_settings

RATE_LIMIT_DETAIL = "Túl sok kérés. Várj egy percet, majd próbáld újra."


class SlidingWindowLimiter:
    """Per-key request counts over a rolling window (monotonic clock)."""

    def __init__(self, max_keys: int = 20_000) -> None:
        self._lock = threading.Lock()
        self._hits: dict[str, deque[float]] = {}
        self._max_keys = max_keys

    def allow(self, key: str, max_requests: int, window_seconds: float) -> tuple[bool, int]:
        """Return (allowed, retry_after_seconds). max_requests <= 0 disables the limit."""
        if max_requests <= 0:
            return True, 0
        now = time.monotonic()
        cutoff = now - window_seconds
        with self._lock:
            if len(self._hits) > self._max_keys:
                stale = [k for k, q in self._hits.items() if not q or q[-1] < cutoff]
                for k in stale:
                    del self._hits[k]
            q = self._hits.setdefault(key, deque())
            while q and q[0] < cutoff:
                q.popleft()
            if len(q) >= max_requests:
                retry = int(q[0] + window_seconds - now) + 1
                return False, max(retry, 1)
            q.append(now)
            return True, 0

    def reset(self) -> None:
        with self._lock:
            self._hits.clear()


limiter = SlidingWindowLimiter()


def client_ip(request: Request) -> str:
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    if request.client and request.client.host:
        return request.client.host
    return "unknown"


def _enforce(request: Request, bucket: str, max_requests: int) -> None:
    settings = get_settings()
    allowed, retry_after = limiter.allow(
        f"{bucket}:{client_ip(request)}",
        max_requests,
        settings.rate_limit_window_seconds,
    )
    if not allowed:
        raise HTTPException(
            status_code=429,
            detail=RATE_LIMIT_DETAIL,
            headers={"Retry-After": str(retry_after)},
        )


def limit_execute(request: Request) -> None:
    _enforce(request, "execute", get_settings().rate_limit_execute_per_minute)


def limit_judge(request: Request) -> None:
    _enforce(request, "judge", get_settings().rate_limit_judge_per_minute)


def limit_feedback(request: Request) -> None:
    _enforce(request, "feedback", get_settings().rate_limit_feedback_per_minute)
