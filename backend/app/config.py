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
    # Comma-separated origins, or * for any (Vercel preview URLs vary).
    cors_origins: str = "*"
    posthog_api_key: str = ""
    posthog_host: str = "https://eu.i.posthog.com"

    def cors_origin_list(self) -> list[str]:
        raw = (self.cors_origins or "*").strip()
        if raw == "*":
            return ["*"]
        return [part.strip() for part in raw.split(",") if part.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
