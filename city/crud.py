from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, select, delete, insert

from . import schemas, models


async def get_all_cities(
        db: AsyncSession
) -> list[schemas.City]:
    query = select(models.DBCity)
    city_list = await db.execute(query)
    return [city[0] for city in city_list.fetchall()]


async def get_city(
        db: AsyncSession, city_id: int
) -> schemas.City:
    query = select(models.DBCity).where(models.DBCity.id == city_id)
    city = await db.execute(query)

    city = city.fetchone()

    if city:
        return city[0]


async def create_city(
        db: AsyncSession, city: schemas.City
) -> dict:
    query = insert(models.DBCity).values(
        name=city.name, additional_info=city.additional_info
    )
    result = await db.execute(query)
    await db.commit()
    resp = {**city.model_dump(), "id": result.lastrowid}
    return resp


async def update_city(
        db: AsyncSession, city_id: int, city: schemas.City
) -> dict:
    query = (
        update(models.DBCity)
        .where(models.DBCity.id == city_id)
        .values(name=city.name, additional_info=city.additional_info)
        .returning(models.DBCity.id)
    )
    result = await db.execute(query)
    await db.commit()
    resp = {**city.model_dump(), "id": result.fetchone().id}
    return resp


async def delete_city(
        db: AsyncSession, city_id: int
) -> None:
    query = delete(models.DBCity).where(models.DBCity.id == city_id)

    await db.execute(query)
    await db.commit()
