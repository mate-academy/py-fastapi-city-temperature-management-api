from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from api_v1.config import settings


engine = create_async_engine(settings.DATABASE_URL, echo=settings.ECHO)

# Prevent attribute expiration on commit to avoid async lazy-loads in response serialization.
SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)
