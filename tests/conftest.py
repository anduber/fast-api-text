"""Pytest fixtures for API testing.

We use httpx's ASGI transport to interact with the FastAPI app without
starting a real HTTP server. The database is reset between tests for isolation.
"""

from __future__ import annotations

import asyncio
import os
from typing import AsyncIterator

import httpx
import pytest

from main import app
from app.db.session import engine
from app.db.base import Base


@pytest.fixture(autouse=True)
def _reset_db() -> None:
    """Drop and recreate tables before each test to ensure isolation."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


@pytest.fixture()
async def client() -> AsyncIterator[httpx.AsyncClient]:
    """Provide an AsyncClient configured for the FastAPI app."""
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as c:
        yield c