from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import City
from cities.schemas import (
    CityUpdateSchema,
    CityCreateSchema,

)
from database import get_db


async def create_city(city: CityCreateSchema, db: AsyncSession = Depends(get_db)):
    new_city = City(**city.model_dump())

    db.add(new_city)
    await db.commit()
    await db.refresh(new_city)
    return new_city


async def get_all_cities(db: AsyncSession = Depends(get_db),
                                       skip: int = 0,
                                       limit: int = 10
                                       ):
    result = await db.execute(select(City).offset(skip).limit(limit))
    cities = result.scalars().all()
    return cities


async def get_city_by_id(city_id: int | None,
                         db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(City).where(city_id == City.id))
    city = result.scalar_one_or_none()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city



async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(City).where(city_id == City.id))
    city = result.scalar_one_or_none()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    await db.delete(city)
    await db.commit()
    return {"message": "City deleted"}


async def update_city(
        city_id: int,
        city_data: CityUpdateSchema,
        db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(City).where(City.id == city_id))
    city = result.scalar_one_or_none()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    for field, value in city_data.model_dump(exclude_unset=True).items():
        setattr(city, field, value)

    await db.commit()
    await db.refresh(city)
    return city
