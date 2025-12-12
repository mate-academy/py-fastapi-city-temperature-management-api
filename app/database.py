from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# SQLite database configuration
SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"

# check_same_thread is required for SQLite when using the same connection in different threads
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """FastAPI dependency that provides a database session per request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

