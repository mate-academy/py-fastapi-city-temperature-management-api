from fastapi import FastAPI

from src.cities.router import router as city_router
from src.temperatures.router import router as temperature_router

app = FastAPI()

app.include_router(city_router)
app.include_router(temperature_router)


@app.get("/")
def root() -> dict:
    return {"message": "Hello World"}
