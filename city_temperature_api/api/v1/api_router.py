from fastapi import APIRouter
from .endpoints import cities, temperatures


router = APIRouter()

router.include_router(
    cities.router, prefix="/cities", tags=["Cities"]
)

router.include_router(
    temperatures.router, prefix="/temperatures", tags=["Temperatures"]
)
