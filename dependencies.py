from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import SessionLocal, engine, Base


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_db_and_tables():
    Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Connecting to DB")
    create_db_and_tables()

    yield

    print("Closing DB")
