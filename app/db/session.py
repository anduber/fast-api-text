from __future__ import annotations

from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.core.config import get_settings
from app.db.base import Base


settings = get_settings()

# Create engine from configured DATABASE_URL
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

# Factory for DB sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency that yields a DB session and ensures cleanup."""
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """Initialize database tables (create if not exist)."""
    Base.metadata.create_all(bind=engine)