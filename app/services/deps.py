from __future__ import annotations

from fastapi import Depends

from app.repositories import get_task_repository, TaskRepository
from app.services.task_service import TaskService


def get_task_service(repo: TaskRepository = Depends(get_task_repository)) -> TaskService:
    """Dependency factory that binds a TaskService to the request-scoped repository."""
    return TaskService(repo)