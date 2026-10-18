from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from cities import models, schemas

async def get_cities(db:AsyncSession) -> list[models.City]:
    cities = await db.scalars(select(models.City))
    return cities.all()

async def create_city(db:AsyncSession, city:schemas.CityCreate) -> models.City:
    db_city = models.City(name=city.name, additional_info=city.additional_info)
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)
    return db_city


async def delete_city(db:AsyncSession, city_id:int) -> bool:
    city = await db.get(models.City, city_id)
    if not city:
        return False

    await db.delete(city)
    await db.commit()

    return True


async def get_city(db:AsyncSession, city_id:int) -> models.City:
    city = await db.get(models.City, city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city

async def update_city(db:AsyncSession, city_id:int, city_update:schemas.CityUpdate) -> models.City:
    city = await db.get(models.City, city_id)

    if city_update is not None:
        city.name = city_update.name
        city.additional_info = city_update.additional_info

    await db.commit()
    await db.refresh(city)
    return city