"""Entrypoint for the FastAPI Task Manager API.

This module creates the FastAPI application, sets up middleware, loads
configuration, and includes the API routers.
"""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import Settings, get_settings
from app.core.security import SecurityHeadersMiddleware
from app.api.routes.tasks import router as tasks_router


def create_app() -> FastAPI:
    """Application factory to create and configure the FastAPI app."""
    settings: Settings = get_settings()

    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.VERSION,
        docs_url="/docs",  # Swagger UI
        redoc_url="/redoc",  # ReDoc
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
