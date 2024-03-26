from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from database import Base, engine, SessionLocal
from endpoints import cities, temperatures
from core.config import settings

app = FastAPI()


def create_tables() -> None:
    try:
        Base.metadata.create_all(bind=engine)
    except SQLAlchemyError as e:
        print(f"Error creating tables: {e}")


def get_db() -> Session:
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
def startup_event() -> None:
    if settings.environment == "development":
        create_tables()


@app.on_event("shutdown")
def shutdown_event() -> None:
    pass


@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(
    request: Request, exc: SQLAlchemyError
) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content={"message": "Database error occurred."},
    )


app.include_router(cities.router)
app.include_router(temperatures.router)
