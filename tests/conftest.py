"""Pytest fixtures for API testing.

We use httpx's ASGI transport to interact with the FastAPI app without
starting a real HTTP server. The task store is reset between tests.
"""

from __future__ import annotations

import asyncio
import os
from typing import AsyncIterator

import httpx
import pytest

from main import app
from app.services.task_service import TaskService


@pytest.fixture(autouse=True)
def _reset_store() -> None:
    """Reset in-memory store before each test to ensure isolation."""
    TaskService.reset_store()


@pytest.fixture()
async def client() -> AsyncIterator[httpx.AsyncClient]:
    """Provide an AsyncClient configured for the FastAPI app."""
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as c:
        yield c