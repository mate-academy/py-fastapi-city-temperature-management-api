from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.city.models import DBCity
from src.city.schemas import CreateCity


async def get_all_cities(db: AsyncSession):
    query = select(DBCity)
    result = await db.execute(query)
    return [city[0]  for city in result.fetchall()]


async def get_city_by_name(db: AsyncSession, city_name: str) -> DBCity:
    query = select(DBCity).where(DBCity.name == city_name)
    result = await db.execute(query)
    city = result.fetchall()
    if city:
        return city[0][0]


async def create_city(db: AsyncSession, city: CreateCity) -> DBCity:
    query = insert(DBCity).values(
        name=city.name,
        additional_info=city.additional_info
    )
    result = await db.execute(query)
    await db.commit()
    resp = {**city.model_dump(), "id": result.inserted_primary_key}
    return resp
