from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from city.models import City
from city.schemas import CityCreateUpdateSchema


async def async_create_new_city(
    db: AsyncSession, city: CityCreateUpdateSchema
) -> City:
    city = City(name=city.name, additional_info=city.additional_info)

    db.add(city)
    await db.commit()
    await db.refresh(city)

    return city


async def async_get_all_cities(db: AsyncSession) -> list[City]:
    cities = await db.scalars(select(City))
    return cities.all()


async def async_get_one_city(db: AsyncSession, city_id: int) -> City:
    city = await db.get(City, city_id)

    if not city:
        raise HTTPException(status_code=400, detail="City not found")

    return city


async def async_update_city(
    db: AsyncSession, city_id: int, pydantic_city: CityCreateUpdateSchema
) -> City:
    city = await db.get(City, city_id)

    if not city:
        raise HTTPException(status_code=400, detail="City not found")

    city.name = pydantic_city.name
    city.additional_info = pydantic_city.additional_info

    await db.commit()
    await db.refresh(city)

    return city


async def async_delete_city(db: AsyncSession, city_id: int) -> dict:
    city = await db.get(City, city_id)

    if not city:
        raise HTTPException(status_code=400, detail="City not found")

    await db.delete(city)
    await db.commit()

    return {"detail": "City deleted"}
