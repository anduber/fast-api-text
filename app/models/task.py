"""Internal Task model used by the service layer.

We keep an internal representation decoupled from the Pydantic schemas
that are exposed at the API boundary. This mirrors common patterns when
using an ORM (e.g., SQLAlchemy), but here we use a simple dataclass for
in-memory storage.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Task:
    """Internal Task model.

    Attributes
    -----------
    id: Unique identifier (auto-incremented in the service layer).
    title: Short title for the task.
    description: Optional longer description.
    is_completed: Whether the task is completed.
    created_at: Timestamp when the task was created.
    updated_at: Timestamp of the last update.
    """

    id: int
    title: str
    description: Optional[str]
    is_completed: bool
    created_at: datetime
    updated_at: datetime