from fastapi import FastAPI

from app.city.routers import router as city_router
from app.temperature.routers import router as temperature_router

app = FastAPI()


app.include_router(city_router, prefix="/cities", tags=["Cities"])
app.include_router(
    temperature_router, prefix="/temperatures", tags=["Temperatures"]
)
