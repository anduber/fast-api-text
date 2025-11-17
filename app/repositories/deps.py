from __future__ import annotations

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from .task_repository import TaskRepository


def get_task_repository(db: Session = Depends(get_db)) -> TaskRepository:
    """Dependency factory that binds a TaskRepository to the request-scoped Session."""
    return TaskRepository(db)