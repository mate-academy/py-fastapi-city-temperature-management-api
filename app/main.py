from fastapi import FastAPI
from app.database import engine, Base
from app.cities.models import City
from app.temperatures.models import Temperature
from app.cities import router as cities_router
from app.temperatures import router as temperatures_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Modular City Weather API",
    description="Refactored FastAPI app following the Package-by-Feature pattern with Pydantic v2 and SQLAlchemy 2.0.",
    version="2.0.0",
)

app.include_router(cities_router.router)
app.include_router(temperatures_router.router)


@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Welcome to Modular Weather Tracker. Go to /docs for testing."
    }
