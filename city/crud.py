from typing import Type

from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession

from city import models, schemas
from city.models import DBCity


async def get_all_cities(db: AsyncSession) -> [models.DBCity]:
    query = select(models.DBCity)
    cities_list = await db.execute(query)
    return [city[0] for city in cities_list.fetchall()]


async def create_city(db: AsyncSession, city: schemas.CityIn) -> dict:
    query = insert(models.DBCity).values(
        name=city.name,
        additional_info=city.additional_info,
    )
    result = await db.execute(query)
    await db.commit()
    response = {**city.model_dump(), "id": result.lastrowid}
    return response


async def get_city(db: AsyncSession, city_id: int) -> Type[DBCity] | None:
    return await db.get(models.DBCity, city_id)


async def update_city(
        db: AsyncSession,
        city_id: int,
        city: schemas.CityIn
) -> dict:
    query = update(models.DBCity).where(models.DBCity.id == city_id).values(
        name=city.name,
        additional_info=city.additional_info
    )
    result = await db.execute(query)
    await db.commit()
    response = {**city.model_dump(), "id": result.lastrowid}
    return response


async def delete_city(db: AsyncSession, city_id: int) -> None:
    db_city = await get_city(db, city_id)
    if db_city:
        await db.delete(db_city)
        await db.commit()
