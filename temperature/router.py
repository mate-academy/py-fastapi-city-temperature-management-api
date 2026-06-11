from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from . import crud
from .schemas import Temperature


router = APIRouter(prefix="/temperatures", tags=["temperatures"])


@router.get("/", response_model=list[Temperature])
async def read_temperatures(city_id: int = None, db: AsyncSession = Depends(get_db)):
    return await crud.get_temperatures(db, city_id)


@router.post("/update")
async def update_temperatures(db: AsyncSession = Depends(get_db)):
    await crud.update_temperatures(db)
    return {"detail": "Temperatures updated successfully"}
