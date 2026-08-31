"""Shared auth for /internal/* ops endpoints (seed, workspace TTL)."""

import secrets

from fastapi import HTTPException, Request

from app.config import get_settings


def require_ops_token(request: Request) -> None:
    """Require X-Cleanup-Token. Missing token → 404 so the route stays hidden."""
    token = get_settings().cleanup_token
    if not token:
        raise HTTPException(status_code=404, detail="Not found")
    provided = request.headers.get("x-cleanup-token") or ""
    if not secrets.compare_digest(provided, token):
        raise HTTPException(status_code=403, detail="Forbidden")
