from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from city.schemas import CityCreate, CityRead
from city.models import City
from city.crud import create_city, get_all_cities, delete_city


router = APIRouter(prefix="/cities", tags=["Cities"])


@router.post("", response_model=CityRead)
async def create(city: CityCreate, db: AsyncSession = Depends(get_db)):
    return await create_city(db, City(**city.model_dump()))


@router.get("", response_model=list[CityRead])
async def list_cities(db: AsyncSession = Depends(get_db)):
    return await get_all_cities(db)


@router.delete("/{city_id}")
async def remove(city_id: int, db: AsyncSession = Depends(get_db)):
    if not await delete_city(db, city_id):
        raise HTTPException(404, "City not found")
    return {"status": "deleted"}