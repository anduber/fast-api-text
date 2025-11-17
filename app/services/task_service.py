"""Service layer providing CRUD operations via a repository.

Routes should depend on the service, and the service depends on
the repository (which itself is bound to the request-scoped DB session).
"""

from __future__ import annotations

from typing import List

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate
from app.repositories import TaskRepository


class TaskNotFoundError(Exception):
    """Raised when a task with a given ID does not exist."""


class TaskService:
    """CRUD operations backed by a repository."""

    def __init__(self, repo: TaskRepository):
        self.repo = repo

    def list_tasks(self) -> List[Task]:
        """Return all tasks as a list (unordered)."""
        return self.repo.list()

    def get_task(self, task_id: int) -> Task:
        """Return a single task by ID or raise TaskNotFoundError."""
        task = self.repo.get(task_id)
        if task is None:
            raise TaskNotFoundError(f"Task with id {task_id} not found")
        return task

    def create_task(self, payload: TaskCreate) -> Task:
        """Create a new task in the database from the provided payload."""
        return self.repo.create(payload)

    def update_task(self, task_id: int, payload: TaskUpdate) -> Task:
        """Update fields on an existing task and return the updated task.

        Supports partial updates: only provided fields are changed.
        """
        existing = self.get_task(task_id)
        return self.repo.update(existing, payload)

    def delete_task(self, task_id: int) -> None:
        """Remove a task by ID or raise TaskNotFoundError if absent."""
        existing = self.get_task(task_id)
        self.repo.delete(existing)