from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from city import models, schemas
from city.models import City


async def get_all_city(db: AsyncSession):
    query = select(models.City)
    city_list = await db.execute(query)
    return [city[0] for city in city_list.fetchall()]


async def create_city(db: AsyncSession, city: schemas.CityBase):
    query = insert(models.City).values(
        name=city.name,
        additional_info=city.additional_info
    )
    results = await db.execute(query)
    await db.commit()
    resp = {
        **city.model_dump(),
        "id": results.lastrowid
    }
    return resp


async def get_city(db: AsyncSession, city_id: int):
    # query = select(models.City).where(models.City.id == city_id)
    # result = await db.execute(query)
    # city = result.scalar_one_or_none()
    city = await db.get(models.City, city_id)
    if city is None:
        return None
    return city


async def update_city(db: AsyncSession, city_id: int, city: schemas.CityBase):
    current_city = await db.get(models.City, city_id)
    if current_city is None:
        return None

    current_city.name = city.name
    current_city.additional_info = city.additional_info
    await db.commit()
    await db.refresh(current_city)

    return current_city


async def delete_city(db: AsyncSession, city_id: int):
    current_city = await db.get(models.City, city_id)
    if current_city is None:
        return None

    await db.delete(current_city)
    await db.commit()
    return current_city
