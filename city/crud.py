from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from city import models, schemas


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
