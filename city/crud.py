from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from city import models, schemas


async def get_all_cities(db: AsyncSession):
    query = select(models.DBCity)
    cities_list = await db.execute(query)

    return [city[0] for city in cities_list.fetchall()]


async def create_city(db: AsyncSession, city: schemas.CityCreate):
    query = insert(models.DBCity).values(
        name=city.name, additional_info=city.additional_info
    )
    result = await db.execute(query)
    await db.commit()
    resp = {**city.model_dump(), "id": result.lastrowid}
    return resp


async def delete_city(db: AsyncSession, city_id: int):
    city = await db.get(models.DBCity, city_id)
    if city:
        await db.delete(city)
        await db.commit()
        return True
    return False
