from fastapi import APIRouter

from app.routers.city import router as city_router
from app.routers.temperature import router as temperature_router

router = APIRouter()
router.include_router(city_router, prefix="/cities", tags=["cities"])
router.include_router(
    temperature_router,
    prefix="/temperatures",
    tags=["temperatures"]
)
