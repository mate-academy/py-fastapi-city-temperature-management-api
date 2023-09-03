from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from . import models, schemas


async def get_all_cities(
        db: AsyncSession, skip: int = 0, limit: int = 100
) -> list[schemas.CityBase]:
    query = select(models.DBCity).offset(skip).limit(limit)
    cities_list = await db.execute(query)
    return [city[0] for city in cities_list.fetchall()]


async def get_city_by_name(db: AsyncSession, city_name: str):
    query = select(models.DBCity).filter(models.DBCity.name == city_name)
    cities = await db.execute(query)
    return cities.first()


async def get_city_by_id(db: AsyncSession, city_id: int):
    stmt = select(models.DBCity).where(models.DBCity.id == city_id)
    result = await db.execute(stmt)
    return result.scalar()


async def create_city(db: AsyncSession, city: schemas.CityCreate) -> dict:
    query = insert(models.DBCity).values(
        name=city.name,
        additional_info=city.additional_info
    )
    result = await db.execute(query)
    await db.commit()
    return {**city.model_dump(), "id": result.lastrowid}


async def update_city(
        db: AsyncSession, city_id: int, city: schemas.CityBase
) -> dict:
    city_to_update = update(models.DBCity).where(models.DBCity.id == city_id).values(
        name=city.name,
        additional_info=city.additional_info
    )
    result = await db.execute(city_to_update)
    await db.commit()
    return {**city.model_dump(), "id": result.lastrowid}


async def delete_city(
        db: AsyncSession, city_id: int
) -> None:
    city_to_delete = delete(models.DBCity).where(models.DBCity.id == city_id)
    await db.execute(city_to_delete)
    await db.commit()
