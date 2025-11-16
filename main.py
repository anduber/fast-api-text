"""Entrypoint for the FastAPI Task Manager API.

This module creates the FastAPI application, sets up middleware, loads
configuration, and includes the API routers.
"""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import Settings, get_settings
from app.core.security import SecurityHeadersMiddleware
from app.api.routes.tasks import router as tasks_router
from app.db.session import init_db, engine


def create_app() -> FastAPI:
    """Application factory to create and configure the FastAPI app."""
    settings: Settings = get_settings()

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # Startup: initialize database tables
        init_db()
        yield
        # Shutdown: dispose SQLAlchemy engine
        engine.dispose()

    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.VERSION,
        docs_url="/docs",  # Swagger UI
        redoc_url="/redoc",  # ReDoc
        lifespan=lifespan,
    )

    # CORS: allow frontend apps to call this API from configured origins
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Basic security headers
    app.add_middleware(SecurityHeadersMiddleware)

    # Include routers
    app.include_router(tasks_router)

    return app


# This is the ASGI application object used by uvicorn/gunicorn
app = create_app()
