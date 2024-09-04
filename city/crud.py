from typing import Sequence

from sqlalchemy.future import select
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from city.models import City
from city.schemas import CityCreate


async def get_cities(db: AsyncSession) -> Sequence[City]:
    result = await db.execute(select(City))
    return result.scalars().all()


async def create_city(db: AsyncSession, city: CityCreate) -> City:
    db_city = City(name=city.name, additional_info=city.additional_info)
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)
    return db_city


async def get_city(db: AsyncSession, city_id: int) -> City:
    city = await db.scalar(select(City).where(City.id == city_id))
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return city


async def delete_city(db: AsyncSession, city_id: int) -> dict:
    action = delete(City).where(City.id == city_id)
    await db.execute(action)
    await db.commit()
    return {"message": "City deleted"}
