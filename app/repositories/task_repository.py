from __future__ import annotations

from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate


class TaskRepository:
    """Repository encapsulating Task persistence operations."""

    def __init__(self, db: Session):
        self.db = db

    def list(self) -> List[Task]:
        return self.db.query(Task).all()

    def get(self, task_id: int) -> Optional[Task]:
        return self.db.get(Task, task_id)

    def create(self, payload: TaskCreate) -> Task:
        now = datetime.now(timezone.utc)
        task = Task(
            title=payload.title,
            description=payload.description,
            is_completed=payload.is_completed,
            created_at=now,
            updated_at=now,
        )
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def update(self, task: Task, payload: TaskUpdate) -> Task:
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
            self.db.add(task)
            self.db.commit()
            self.db.refresh(task)
        return task

    def delete(self, task: Task) -> None:
        self.db.delete(task)
        self.db.commit()
