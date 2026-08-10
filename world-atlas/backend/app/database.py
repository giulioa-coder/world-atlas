"""
Database connection and session management.

Uses SQLAlchemy 2.0 with async support.
Supports both PostgreSQL (with JSONB) and SQLite (with JSON).
"""

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.types import TypeDecorator, JSON

from app.core.config import settings


class JSONBOrJSON(TypeDecorator):
    """
    Custom type that uses JSONB for PostgreSQL and JSON for SQLite.
    This allows the same models to work with both databases.
    """
    impl = JSON
    cache_ok = True
    
    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(JSONB())
        else:
            return dialect.type_descriptor(JSON())
    
    def process_bind_param(self, value, dialect):
        return value
    
    def process_result_value(self, value, dialect):
        return value


# Create database engine
# Support SQLite file paths that start with sqlite:///
db_url = settings.DATABASE_URL
if db_url.startswith('sqlite:///'):
    engine = create_engine(
        db_url,
        echo=settings.DEBUG,
        connect_args={"check_same_thread": False},  # Needed for SQLite
    )
else:
    engine = create_engine(
        db_url,
        echo=settings.DEBUG,
        pool_pre_ping=True,
    )

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Base class for models
Base = declarative_base()


def get_db():
    """Dependency for getting database sessions."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
