from fastapi import FastAPI
from src.city_weather.routers import city_router, temperature_router

app = FastAPI()

app.include_router(city_router)
app.include_router(temperature_router)
