from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession

from . import models, schemas


async def get_all_cities(db: AsyncSession):
    query = select(models.DBCity)
    cities_list = await db.execute(query)
    return [city[0] for city in cities_list.fetchall()]


async def create_city(db: AsyncSession, city: schemas.CityBase):
    query = insert(models.DBCity).values(
        name=city.name,
        additional_info=city.additional_info,
    )
    result = await db.execute(query)
    await db.commit()
    resp = {**city.model_dump(), "id": result.lastrowid}
    return resp


async def delete_city(db: AsyncSession, city_id: int):
    query = delete(models.DBCity).where(models.DBCity.id == city_id)
    await db.execute(query)
    await db.commit()
    return {"message": "City deleted"}
