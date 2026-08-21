"""
Database configuration.

Uses SQLite for simplicity (zero external setup required). The engine, session
factory, and declarative base live here so both `models.py` and the routers
can import from a single source of truth.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./weather_app.db"

# `check_same_thread=False` is required for SQLite when it's accessed from
# more than one thread, which happens under FastAPI's threaded request
# handling (sync path operations run in a threadpool).
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """
    FastAPI dependency that yields a database session and guarantees it is
    closed after the request finishes, even if an exception is raised.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
