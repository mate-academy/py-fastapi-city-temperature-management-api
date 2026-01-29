from city.router import city_router
from temperature.router import temperature_router
from fastapi import FastAPI

app = FastAPI()
app.include_router(city_router, prefix="", tags=["city"])
app.include_router(temperature_router, prefix="", tags=["temperature"])
