from fastapi import FastAPI

from src.city_app.router import city_router
from src.temperature_app.routers import temp_router

app = FastAPI()


app.include_router(city_router)
app.include_router(temp_router)