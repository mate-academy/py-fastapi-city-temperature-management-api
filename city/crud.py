from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, select, delete, insert

from . import schemas, models


async def get_all_cities(db: AsyncSession):
    query = select(models.DBCity)
    city_list = await db.execute(query)
    return [city[0] for city in city_list.fetchall()]


async def get_city_by_name(db: AsyncSession, name: str):
    query = select(models.DBCity).where(models.DBCity.name == name)
    result = await db.execute(query)
    city = result.fetchone()
    if city:
        return city[0]


async def get_city_by_id(db: AsyncSession, city_id: int):
    query = select(models.DBCity).where(models.DBCity.id == city_id)
    result = await db.execute(query)
    city = result.fetchone()
    if city:
        return city[0]


async def create_city(db: AsyncSession, city: schemas.City):
    query = insert(models.DBCity).values(
        name=city.name,
        additional_info=city.additional_info,
    )
    result = await db.execute(query)
    await db.commit()
    response = {**city.model_dump(), "id": result.lastrowid}
    return response


async def update_city(db: AsyncSession, city_id: int, city: schemas.City):
    query = (
        update(
            models.DBCity
        ).where(models.DBCity.id == city_id).
        values(
            name=city.name,
            additional_info=city.additional_info,
        ).returning(
            models.DBCity.id
        )
    )
    result = await db.execute(query)
    await db.commit()
    response = {**city.model_dump(), "id": result.all()[0][0]}
    return response


async def delete_city(db: AsyncSession, city_id: int):
    query = (
        delete(models.DBCity).
        where(models.DBCity.id == city_id).
        returning(models.DBCity)
    )
    await db.execute(query)
    await db.commit()
