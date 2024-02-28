from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies import get_db
from src.temperature import service

router = APIRouter(
    prefix="/temperatures",
    tags=["temperatures"],
)


DBDepend = Depends(get_db)


@router.post("/update")
async def update_temperatures(db: AsyncSession = DBDepend):
    return await service.update_temperature_for_cities(db=db)


@router.get("/")
async def get_temperatures(db: AsyncSession = DBDepend, city_id: int | None = None):
    return await service.get_all_temperatures(city_id=city_id, db=db)
