from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from city import models, schemas


async def get_all_cities(db: AsyncSession):
    query = select(models.City)
    cities_list = await db.execute(query)
    return [city[0] for city in cities_list.fetchall()]


async def create_city(db: AsyncSession, city: schemas.CityCreate):
    query = insert(models.City).values(
        name=city.name,
        additional_info=city.additional_info,
    )
    result = await db.execute(query)
    await db.commit()
    resp = {**city.model_dump(), "id": result.lastrowid}
    return resp


async def delete_city(db: AsyncSession, city_id: int) -> bool:
    result = await db.execute(
        select(models.City).filter(models.City.id == city_id)
    )
    db_city = result.scalar_one_or_none()
    if db_city:
        await db.delete(db_city)
        await db.commit()
        return True
    return False
