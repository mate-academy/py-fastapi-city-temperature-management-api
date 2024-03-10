from __future__ import annotations

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from typing import List, Dict

from city import models, schemas
from dependenci import CommonsDep


async def get_all_cities(
    db: AsyncSession, commons: CommonsDep | None
) -> List[models.CityDB]:
    query = select(models.CityDB)
    if commons:
        if commons.get("q"):
            query = query.filter(models.CityDB.name.ilike(f"%{commons['q']}%"))
        query = query.offset(commons.get("skip", 0)).limit(commons.get("limit", 100))
    cities_list = await db.execute(query)
    return [city for city in cities_list.scalars()]


async def create_city(db: AsyncSession, city: schems.CityCreate) -> Dict[str, None]:
    query = insert(models.CityDB).values(
        name=city.name, additional_info=city.additional_info
    )
    result = await db.execute(query)
    await db.commit()
    resp = {**city.model_dump(), "id": result.lastrowid}
    return resp


async def get_city_by_id(db: AsyncSession, city_id: int) -> models.CityDB | None:
    query = select(models.CityDB).filter(models.CityDB.id == city_id)
    result = await db.execute(query)

    city = result.scalar_one_or_none()

    return city


async def update_city(
    db: AsyncSession, city_id: int, updated_city: schems.CityUpdate
) -> models.CityDB:
    query = select(models.CityDB).filter(models.CityDB.id == city_id)
    result = await db.execute(query)

    city = result.scalar_one_or_none()

    if city:
        for key, value in updated_city.model_dump().items():
            if hasattr(city, key):
                setattr(city, key, value)
        await db.commit()
        await db.refresh(city)

    return city


async def delete_city(db: AsyncSession, city_id: int):
    query = (
        select(models.CityDB)
        .options(joinedload(models.CityDB.temperature))
        .filter(models.CityDB.id == city_id)
    )
    result = await db.execute(query)

    city = result.scalars().first()

    if city:
        for temperature in city.temperature:
            await db.delete(temperature)
        await db.delete(city)
        await db.commit()

    return "City has been deleted successfully"
