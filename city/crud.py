from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from city.models import DBCity
from city.schemas import CityCreate


async def get_all_city(db: AsyncSession):
    query = select(DBCity)
    city_list = await db.execute(query)
    return [city[0] for city in city_list.fetchall()]


async def get_city_by_name(db: AsyncSession, name: str):
    query = select(DBCity).filter(DBCity.name == name)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def get_city_by_id(db: AsyncSession, city_id: int):
    query = select(DBCity).filter(DBCity.id == city_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def create_city(db: AsyncSession, city: CityCreate):
    query = insert(DBCity).values(
        name=city.name,
        additional_info=city.additional_info,
    )
    result = await db.execute(query)
    await db.commit()
    resp = {**city.model_dump(), "id": result.lastrowid}
    return resp
