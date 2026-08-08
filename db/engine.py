from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session
from collections.abc import Generator


SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite3"

engine = create_engine(SQLALCHEMY_DATABASE_URI, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass


def get_db() -> Generator[Session, None, None]:
    with SessionLocal() as session:
        yield session
