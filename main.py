from fastapi import FastAPI
from app.cities.router import router as cities_router
from app.database import engine, Base
from app.temperatures.models import Temperature  # noqa: F401
from app.cities.models import City  # noqa: F401
from app.temperatures.router import router as temperatures_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="City Weather History API",
    description="CRUD API for cities and temperature history.",
    version="1.0.0",
)

app.include_router(cities_router)
app.include_router(temperatures_router)
