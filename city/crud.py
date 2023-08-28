from typing import List

import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from city import models, schemas
from temperature.router import API_KEY, WEATHER_API_URL


async def get_all_cities(
        db: AsyncSession,
        skip: int,
        limit: int
) -> List[models.City]:
    cities = await db.execute(
        select(models.City).offset(skip).limit(limit)
    )
    return [city[0] for city in cities.fetchall()]


async def get_city_by_name(
        db: AsyncSession,
        name: str
) -> models.City:
    city = await db.execute(
        select(models.City).where(models.City.name == name)
    )
    return city.scalar()


async def check_correct_city_name(name: str) -> bool:
    async with httpx.AsyncClient() as client:
        params = {
            "key": API_KEY,
            "q": name
        }
        response = await client.get(url=WEATHER_API_URL, params=params)
        return response.status_code != 200


async def get_city(
        db: AsyncSession,
        city_id: int
) -> models.City:
    city = await db.execute(
        select(
            models.City
        ).where(
            models.City.id == city_id
        )
    )
    return city.scalar()


async def create_city(
        db: AsyncSession,
        city: schemas.CityCreate
) -> models.City:
    new_city = models.City(**city.model_dump())
    db.add(new_city)
    await db.commit()
    await db.refresh(new_city)
    return new_city


async def update_city(
        db: AsyncSession,
        city: models.City,
        city_update: schemas.CityCreate
) -> models.City:
    for key, value in city_update.model_dump().items():
        setattr(city, key, value)
    await db.commit()
    await db.refresh(city)
    return city


async def delete_city(
        db: AsyncSession,
        city: models.City
) -> None:
    city_delete = delete(models.City).where(models.City.id == city.id)
    await db.execute(city_delete)
    await db.commit()
