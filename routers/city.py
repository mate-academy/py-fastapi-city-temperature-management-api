from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from schemas.city import CityCreate, CityRead
from crud.city import create_city, get_cities, get_city, delete_city

router = APIRouter(prefix="/cities", tags=["cities"])


@router.post("", response_model=CityRead)
async def create(city: CityCreate, db: AsyncSession = Depends(get_db)):
    return await create_city(db, city.name, city.additional_info)


@router.get("", response_model=list[CityRead])
async def list_cities(db: AsyncSession = Depends(get_db)):
    return await get_cities(db)


@router.delete("/{city_id}")
async def remove(city_id: int, db: AsyncSession = Depends(get_db)):
    city = await get_city(db, city_id)
    if not city:
        raise HTTPException(404, "City not found")

    await delete_city(db, city)
    return {"ok": True}
