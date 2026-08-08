from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase


SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite3"

engine = create_engine(SQLALCHEMY_DATABASE_URI, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass
