from typing import Any, Callable

from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession

from . import models, schemas


async def get_all_cities(db: AsyncSession) -> list[models.City]:
    query = select(models.City)
    city_list = await db.execute(query)
    return [city[0] for city in city_list.fetchall()]


async def create_city(
        db: AsyncSession,
        city: schemas.CityCreate
) -> dict[str, Any]:
    query = insert(models.City).values(**city.dict())
    result = await db.execute(query)
    await db.commit()
    response = {"id": result.lastrowid, **city.model_dump()}
    return response


async def get_city_by_id(
        db: AsyncSession,
        city_id: int
) -> models.City | None:
    query = select(models.City, models.City.id).where(
        models.City.id == city_id
    )
    result = await db.execute(query)
    city = result.scalars().first()
    return city if city else None


async def update_city(
        db: AsyncSession,
        city_id: int,
        city_update: schemas.CityCreate
) -> models.City | None:
    city = await db.get(models.City, city_id)
    if city is None:
        return None

    for field, value in city_update.dict().items():
        setattr(city, field, value)

    await db.commit()
    await db.refresh(city)

    return city


async def delete_city(
        db: AsyncSession,
        city_id: int
) -> Callable[[], int]:
    query = delete(models.City).where(models.City.id == city_id)
    result = await db.execute(query)
    await db.commit()
    return result.rowcount
