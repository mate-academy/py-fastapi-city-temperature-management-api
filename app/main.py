from fastapi import FastAPI
from app.database import engine, Base

from app.cities.models import City
from app.temperatures.models import Temperature
from app.cities.router import router as cities_router
from app.temperatures.router import router as temperatures_router

_tables = (City, Temperature)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="City Weather Service")

app.include_router(cities_router)
app.include_router(temperatures_router)


@app.get("/")
def read_root():
    return {"message": "Welcome to City Weather Service API!"}
