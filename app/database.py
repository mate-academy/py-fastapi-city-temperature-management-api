from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

# Note: DeclarativeBase requires SQLAlchemy >= 2.0
# See requirements.txt: sqlalchemy>=2.0.36

# URL for async SQLite (requires aiosqlite)
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./cities.db"

# Create async engine
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True  # Output SQL queries to console (for development)
)

# Create session factory for async operations
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base class for models (SQLAlchemy 2.0 style)
# DeclarativeBase is the modern SQLAlchemy 2.0 API
# For SQLAlchemy < 2.0, use: from sqlalchemy.ext.declarative import declarative_base
#
# Note: Database tables (City, Temperature) are created automatically on application startup
# See app/main.py startup() event handler: Base.metadata.create_all()
class Base(DeclarativeBase):
    pass


# Dependency injection for getting database session
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session