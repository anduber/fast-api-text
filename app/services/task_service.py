"""Service layer providing CRUD operations for tasks using SQLAlchemy."""

from __future__ import annotations

from datetime import datetime
from typing import List

from sqlalchemy.orm import Session

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate


class TaskNotFoundError(Exception):
    """Raised when a task with a given ID does not exist."""


class TaskService:
    """CRUD operations backed by a database session."""

    @staticmethod
    def list_tasks(db: Session) -> List[Task]:
        """Return all tasks as a list (unordered)."""
        return db.query(Task).all()

    @staticmethod
    def get_task(db: Session, task_id: int) -> Task:
        """Return a single task by ID or raise TaskNotFoundError."""
        task = db.get(Task, task_id)
        if task is None:
            raise TaskNotFoundError(f"Task with id {task_id} not found")
        return task

    @staticmethod
    def create_task(db: Session, payload: TaskCreate) -> Task:
        """Create a new task in the database from the provided payload."""
        now = datetime.utcnow()
        task = Task(
            title=payload.title,
            description=payload.description,
            is_completed=payload.is_completed,
            created_at=now,
            updated_at=now,
        )
        db.add(task)
        db.commit()
        db.refresh(task)
        return task

    @staticmethod
    def update_task(db: Session, task_id: int, payload: TaskUpdate) -> Task:
        """Update fields on an existing task and return the updated task.

        Supports partial updates: only provided fields are changed.
        """
        task = TaskService.get_task(db, task_id)
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
            db.add(task)
            db.commit()
            db.refresh(task)
        return task

    @staticmethod
    def delete_task(db: Session, task_id: int) -> None:
        """Remove a task by ID or raise TaskNotFoundError if absent."""
        task = TaskService.get_task(db, task_id)
        db.delete(task)
        db.commit()