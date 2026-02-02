from fastapi import APIRouter

from app.api.v1.endpoints.cities import router as cities_router
from app.api.v1.endpoints.temperatures import router as temperatures_router

api_router = APIRouter()
api_router.include_router(cities_router)
api_router.include_router(temperatures_router)
