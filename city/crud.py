from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from . import models

from . import schemas

async def get_all_cities(db: AsyncSession):
    query = select(models.City)
    cities = await db.execute(query)
    return [city[0] for city in cities.fetchall()]

async def create_city(db: AsyncSession, city: schemas.CityBase):
    query = insert(models.City).values(
        name=city.name,
        additional_info=city.additional_info,
    )
    result = await db.execute(query)
    await db.commit()
    resp = {**city.model_dump(), "id": result.lastrowid}
    return resp
