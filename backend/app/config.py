from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

_ROOT_ENV = Path(__file__).resolve().parents[2] / ".env"
_LOCAL_ENV = Path(".env")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(str(_ROOT_ENV), str(_LOCAL_ENV)),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database_url: str = "sqlite:///./data/erettsegi.db"
    workspaces_root: str = "/tmp/erettsegi-workspaces"
    executor_image: str = "erettsegi-executor:latest"
    execution_timeout_seconds: int = 5
    execution_memory_limit: str = "128m"
    execution_cpu_limit: str = "0.5"
    execution_backend: str = "subprocess"  # docker | subprocess
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    ai_generation_enabled: bool = False
    # Comma-separated browser origins allowed to call the API directly.
    # Local default is localhost; production Cloud Run must set the Vercel origin (not *).
    cors_origins: str = "http://localhost:3000,http://127.0.0.1:3000"
    # Optional extra regex (e.g. https://.*\\.vercel\\.app for preview URLs). Empty = off.
    cors_origin_regex: str = ""
    rate_limit_execute_per_minute: int = 30
    rate_limit_judge_per_minute: int = 12
    rate_limit_window_seconds: int = 60
    workspace_ttl_days: int = 7
    cleanup_token: str = ""

    def cors_origin_list(self) -> list[str]:
        raw = (self.cors_origins or "").strip()
        if not raw or raw == "*":
            return ["*"]
        return [part.strip() for part in raw.split(",") if part.strip()]

    def cors_middleware_kwargs(self) -> dict:
        origins = self.cors_origin_list()
        regex = (self.cors_origin_regex or "").strip() or None
        return {
            "allow_origins": origins,
            "allow_origin_regex": regex,
            "allow_credentials": False,
            "allow_methods": ["*"],
            "allow_headers": ["*"],
        }


@lru_cache
def get_settings() -> Settings:
    return Settings()
