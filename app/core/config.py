"""Application configuration utilities.

This module loads environment variables and exposes a `Settings` object
used throughout the application to configure behavior (e.g., CORS, debug).

We intentionally avoid `pydantic-settings` to keep dependencies minimal
and rely on `python-dotenv` plus a small `pydantic.BaseModel` for validation.
"""

from __future__ import annotations

import os
from functools import lru_cache
from typing import List

from dotenv import load_dotenv
from pydantic import BaseModel, Field

# Load variables from a local `.env` file if present
load_dotenv()


def _parse_bool(value: str | None, default: bool) -> bool:
    """Parse a boolean environment variable value.

    Accepts values like "true", "1", "yes" for True and "false", "0", "no" for False.
    Falls back to the provided default when value is None.
    """
    if value is None:
        return default
    val = value.strip().lower()
    if val in {"true", "1", "yes", "y"}:
        return True
    if val in {"false", "0", "no", "n"}:
        return False
    return default


def _parse_origins(value: str | None, default: List[str]) -> List[str]:
    """Parse a comma-separated list of origins into a list of strings.

    If value is "*", return ["*"]. Empty entries are ignored.
    """
    if value is None:
        return default
    v = value.strip()
    if v == "*":
        return ["*"]
    return [item.strip() for item in v.split(",") if item.strip()]


class Settings(BaseModel):
    """Application settings loaded from environment variables.

    Attributes
    -----------
    APP_NAME: Human-friendly application name for documentation.
    VERSION: Static version string; adjust as needed.
    ENVIRONMENT: Environment name (development|production|staging|test).
    DEBUG: Enables verbose logging and detailed error pages in development.
    ALLOWED_ORIGINS: List of origins allowed by CORS middleware.
    """

    APP_NAME: str = Field(default=os.getenv("APP_NAME", "Task Manager API"))
    VERSION: str = Field(default=os.getenv("VERSION", "1.0.0"))
    ENVIRONMENT: str = Field(default=os.getenv("ENVIRONMENT", "development"))
    DEBUG: bool = Field(default=_parse_bool(os.getenv("DEBUG"), default=False))
    ALLOWED_ORIGINS: List[str] = Field(default=_parse_origins(os.getenv("ALLOWED_ORIGINS"), default=["*"]))


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return a cached `Settings` instance.

    Using LRU cache avoids repeatedly parsing environment values.
    """
    return Settings()