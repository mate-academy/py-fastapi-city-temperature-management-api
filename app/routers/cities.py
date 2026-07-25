from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models import City
from app.schemas import CityCreate, CityResponse, CityUpdate

router = APIRouter(prefix="/cities", tags=["Cities"])


@router.post("", response_model=CityResponse, status_code=status.HTTP_201_CREATED)
async def create_city(city: CityCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(City).where(City.name == city.name))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="City already exists")

    db_city = City(name=city.name, additional_info=city.additional_info)
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)
    return db_city


@router.get("", response_model=List[CityResponse])
async def get_cities(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(City))
    return result.scalars().all()


@router.get("/{city_id}", response_model=CityResponse)
async def get_city(city_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(City).where(City.id == city_id))
    city = result.scalar_one_or_none()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@router.put("/{city_id}", response_model=CityResponse)
async def update_city(city_id: int, city_update: CityUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(City).where(City.id == city_id))
    city = result.scalar_one_or_none()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    update_data = city_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(city, key, value)

    await db.commit()
    await db.refresh(city)
    return city


@router.delete("/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(City).where(City.id == city_id))
    city = result.scalar_one_or_none()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    await db.delete(city)
    await db.commit()
    return None
