from fastapi import FastAPI

from src.weatherapi.routers.city import city_router
from src.weatherapi.routers.temperature import temperature_router

app = FastAPI()
app.include_router(city_router)
app.include_router(temperature_router)


@app.get("/")
async def root() -> dict:
    return {"message": "Weather API"}
