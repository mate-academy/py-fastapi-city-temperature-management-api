from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from city import models
from city.schemas import CityCreate, CityUpdate


async def get_all_cities(db: AsyncSession):
    query = select(models.DBCity)
    cities_list = await db.execute(query)
    return cities_list.scalars().all()


async def get_city(db: AsyncSession, city_id: int):
    return await db.scalar(select(models.DBCity)
                           .where(models.DBCity.id == city_id))


async def create_city(db: AsyncSession, city: CityCreate):
    db_city = models.DBCity(**city.model_dump())
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)
    return db_city


async def update_city(db: AsyncSession, data: CityUpdate, city_id: int):
    city = await db.get(models.DBCity, city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(city, field, value)

    await db.commit()
    await db.refresh(city)
    return city


async def delete_city(db: AsyncSession, city_id: int):
    city = await db.get(models.DBCity, city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    await db.delete(city)
    await db.commit()
    return city
