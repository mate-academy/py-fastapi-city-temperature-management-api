from fastapi import FastAPI
from app.city.routers import city_router
from app.temperature.routers import temperature_router

app = FastAPI()

app.include_router(city_router, prefix="/cities", tags=["Cities"])
app.include_router(temperature_router, prefix="/temperatures", tags=["Temperatures"])
