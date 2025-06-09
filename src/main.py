from fastapi import FastAPI

from src.cities.router import router as cities_router
from src.temperature.router import router as temperature_router

app = FastAPI()

app.include_router(cities_router, prefix="/api")
app.include_router(temperature_router, prefix="/api")


@app.get("/")
def root():
    return {"message": "Hello"}