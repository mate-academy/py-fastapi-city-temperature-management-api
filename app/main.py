from fastapi import FastAPI
from app.cities.router import router as cities_router
from app.temperatures.router import router as temperatures_router

app = FastAPI(
    title="Weather Tracker API",
    description="A FastAPI application for managing cities and tracking their temperature data.",
    version="1.0.0",
)

app.include_router(cities_router)
app.include_router(temperatures_router)
