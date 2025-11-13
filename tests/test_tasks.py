"""Unit tests for Task API endpoints.

Tests cover create, read, list, update, delete, and not-found cases.
"""

from __future__ import annotations

from typing import Any, Dict

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_task(client: AsyncClient) -> None:
    payload = {"title": "Write docs", "description": "Document the API", "is_completed": False}
    resp = await client.post("/tasks/", json=payload)
    assert resp.status_code == 201
    data = resp.json()
    assert data["id"] == 1
    assert data["title"] == "Write docs"
    assert data["is_completed"] is False


@pytest.mark.asyncio
async def test_get_task(client: AsyncClient) -> None:
    create = await client.post("/tasks/", json={"title": "Learn FastAPI"})
    tid = create.json()["id"]

    resp = await client.get(f"/tasks/{tid}")
    assert resp.status_code == 200
    assert resp.json()["id"] == tid


@pytest.mark.asyncio
async def test_list_tasks(client: AsyncClient) -> None:
    await client.post("/tasks/", json={"title": "Task A"})
    await client.post("/tasks/", json={"title": "Task B"})

    resp = await client.get("/tasks/")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) == 2


@pytest.mark.asyncio
async def test_update_task(client: AsyncClient) -> None:
    create = await client.post("/tasks/", json={"title": "Initial"})
    tid = create.json()["id"]

    resp = await client.put(f"/tasks/{tid}", json={"title": "Updated", "is_completed": True})
    assert resp.status_code == 200
    data = resp.json()
    assert data["title"] == "Updated"
    assert data["is_completed"] is True


@pytest.mark.asyncio
async def test_delete_task(client: AsyncClient) -> None:
    create = await client.post("/tasks/", json={"title": "To be deleted"})
    tid = create.json()["id"]

    resp = await client.delete(f"/tasks/{tid}")
    assert resp.status_code == 204

    # Confirm 404 after deletion
    resp2 = await client.get(f"/tasks/{tid}")
    assert resp2.status_code == 404


@pytest.mark.asyncio
async def test_get_not_found(client: AsyncClient) -> None:
    resp = await client.get("/tasks/9999")
    assert resp.status_code == 404