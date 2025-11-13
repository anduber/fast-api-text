"""Service layer providing CRUD operations for tasks.

This module maintains an in-memory store of tasks. In a real-world
application, this layer would interact with a database or external service.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Dict, List

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate


class TaskNotFoundError(Exception):
    """Raised when a task with a given ID does not exist."""


class TaskService:
    """CRUD operations on the in-memory task store."""

    # In-memory storage: dictionary of tasks keyed by their ID
    _tasks: Dict[int, Task] = {}
    _next_id: int = 1

    @classmethod
    def list_tasks(cls) -> List[Task]:
        """Return all tasks as a list (unordered)."""
        return list(cls._tasks.values())

    @classmethod
    def get_task(cls, task_id: int) -> Task:
        """Return a single task by ID or raise TaskNotFoundError."""
        task = cls._tasks.get(task_id)
        if task is None:
            raise TaskNotFoundError(f"Task with id {task_id} not found")
        return task

    @classmethod
    def create_task(cls, payload: TaskCreate) -> Task:
        """Create a new task from the provided payload and store it."""
        now = datetime.now(timezone.utc)
        task = Task(
            id=cls._next_id,
            title=payload.title,
            description=payload.description,
            is_completed=payload.is_completed,
            created_at=now,
            updated_at=now,
        )
        cls._tasks[task.id] = task
        cls._next_id += 1
        return task

    @classmethod
    def update_task(cls, task_id: int, payload: TaskUpdate) -> Task:
        """Update fields on an existing task and return the updated task.

        Supports partial updates: only provided fields are changed.
        """
        task = cls.get_task(task_id)
        changed = False
        if payload.title is not None:
            task.title = payload.title
            changed = True
        if payload.description is not None:
            task.description = payload.description
            changed = True
        if payload.is_completed is not None:
            task.is_completed = payload.is_completed
            changed = True
        if changed:
            task.updated_at = datetime.utcnow()
            cls._tasks[task.id] = task
        return task

    @classmethod
    def delete_task(cls, task_id: int) -> None:
        """Remove a task by ID or raise TaskNotFoundError if absent."""
        if task_id not in cls._tasks:
            raise TaskNotFoundError(f"Task with id {task_id} not found")
        del cls._tasks[task_id]

    # Test utility: reset store between tests to avoid cross-test pollution
    @classmethod
    def reset_store(cls) -> None:
        """Clear the in-memory store and reset ID counter (for tests)."""
        cls._tasks.clear()
        cls._next_id = 1