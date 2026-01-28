from fastapi import FastAPI

from src.city.router import router as city_router
from src.temperature.router import router as temp_router

app = FastAPI()
app.include_router(city_router, tags=["Cities"])
app.include_router(temp_router, tags=["Temperatures"])
