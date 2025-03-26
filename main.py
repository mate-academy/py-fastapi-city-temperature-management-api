from fastapi import FastAPI

from city.router import router as city_router
from temperature.routers import router as temp_router

app = FastAPI()
app.include_router(city_router, tags=["city"], prefix="/cities")
app.include_router(temp_router, tags=["temperature"], prefix="/temperatures")
