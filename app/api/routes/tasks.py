"""Task API routes implementing CRUD operations.

This module wires HTTP endpoints to service-layer operations and handles
error translation to HTTP responses.
"""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path, Response, status
from sqlalchemy.orm import Session

from app.schemas.task import TaskCreate, TaskRead, TaskUpdate
from app.services.task_service import TaskNotFoundError, TaskService
from app.db.session import get_db


router = APIRouter(prefix="/tasks", tags=["tasks"])


def _to_schema(task) -> TaskRead:
    """Convert internal `Task` model to `TaskRead` schema."""
    return TaskRead(
        id=task.id,
        title=task.title,
        description=task.description,
        is_completed=task.is_completed,
        created_at=task.created_at,
        updated_at=task.updated_at,
    )


@router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate, db: Session = Depends(get_db)) -> TaskRead:
    """Create a new task.

    Returns the created task with its generated ID.
    """
    task = TaskService.create_task(db, payload)
    return _to_schema(task)


@router.get("/", response_model=List[TaskRead])
def list_tasks(db: Session = Depends(get_db)) -> List[TaskRead]:
    """Return a list of all tasks."""
    tasks = TaskService.list_tasks(db)
    return [_to_schema(t) for t in tasks]


@router.get("/{task_id}", response_model=TaskRead)
def get_task(task_id: int = Path(..., ge=1), db: Session = Depends(get_db)) -> TaskRead:
    """Get a single task by its ID or 404 if not found."""
    try:
        task = TaskService.get_task(db, task_id)
    except TaskNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    return _to_schema(task)


@router.put("/{task_id}", response_model=TaskRead)
def update_task(
    task_id: int = Path(..., ge=1),
    payload: TaskUpdate | None = None,
    db: Session = Depends(get_db),
) -> TaskRead:
    """Update fields on an existing task.

    Accepts a partial payload; unspecified fields remain unchanged.
    """
    try:
        task = TaskService.update_task(db, task_id, payload or TaskUpdate())
    except TaskNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    return _to_schema(task)


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
def delete_task(task_id: int = Path(..., ge=1), db: Session = Depends(get_db)) -> Response:
    """Delete a task by ID. Returns 204 on success, 404 if not found."""
    try:
        TaskService.delete_task(db, task_id)
    except TaskNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    return Response(status_code=status.HTTP_204_NO_CONTENT)