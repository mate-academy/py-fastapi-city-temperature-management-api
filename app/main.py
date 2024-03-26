from fastapi import FastAPI
from sqlalchemy.exc import SQLAlchemyError
from database import Base, engine, SessionLocal
from endpoints import cities, temperatures
from core.config import settings
from fastapi.responses import JSONResponse


def create_tables():
    try:
        Base.metadata.create_all(bind=engine)
    except SQLAlchemyError as e:
        print(f"Error creating tables: {e}")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()


@app.on_event("startup")
def startup_event():
    if settings.environment == "development":
        create_tables()
    # Additional startup actions can be added here


@app.on_event("shutdown")
def shutdown_event():
    # Cleanup actions can be added here
    pass


@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={"message": "Database error occurred."},
    )

app.include_router(cities.router)
app.include_router(temperatures.router)
