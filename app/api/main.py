from fastapi import APIRouter

from app.api.routes import city, temperature


api_router = APIRouter()
api_router.include_router(city.router, prefix="/cities", tags=["cities"])
api_router.include_router(
    temperature.router, prefix="/temperatures", tags=["temperatures"]
)
