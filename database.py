from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from settings import settings


engine = create_engine(
    settings.DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(bind=engine, autoflush=False)


class Base(DeclarativeBase):
    pass
