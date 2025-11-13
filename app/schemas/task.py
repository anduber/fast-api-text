"""Pydantic schemas for Task API.

These models define how data is validated on input and serialized on
output. They ensure consistent structure and perform basic sanitation
like trimming whitespace.
"""

from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, Field, field_validator


class TaskBase(BaseModel):
    """Shared fields for creating and reading tasks."""

    title: str = Field(..., min_length=1, max_length=100, description="Short task title")
    description: str | None = Field(
        None, max_length=1000, description="Optional detailed description"
    )
    is_completed: bool = Field(default=False, description="Completion status")

    @field_validator("title")
    @classmethod
    def _strip_title(cls, v: str) -> str:
        """Trim whitespace from title to avoid accidental leading/trailing spaces."""
        return v.strip()


class TaskCreate(TaskBase):
    """Model used for creating a task (request body)."""

    pass


class TaskUpdate(BaseModel):
    """Model used for updating a task.

    All fields are optional to allow partial updates.
    """

    title: str | None = Field(None, min_length=1, max_length=100)
    description: str | None = Field(None, max_length=1000)
    is_completed: bool | None = None

    @field_validator("title")
    @classmethod
    def _strip_title_optional(cls, v: str | None) -> str | None:
        return v.strip() if v is not None else v


class TaskRead(TaskBase):
    """Model used for returning a task in responses."""

    id: int
    created_at: datetime
    updated_at: datetime