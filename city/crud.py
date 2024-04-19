from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

from city import models
from city import schemas


async def get_all_cities(db: AsyncSession):
    query = select(models.DBCity)
    cities_list = await db.execute(query)
    return [city[0] for city in cities_list.fetchall()]


async def get_city_by_name(db: AsyncSession, name: str):
    query = select(models.DBCity).filter(models.DBCity.name == name)
    result = await db.execute(query)
    return result.scalars().first()


async def create_city(db: AsyncSession, city: schemas.CityCreate):
    db_city = models.DBCity(
        name=city.name,
        additional_info=city.additional_info,
    )
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)
    return db_city


async def delete_city(db: AsyncSession, city_id: int):
    result = await db.execute(models.DBCity.delete().where(models.DBCity.id == city_id))
    return result.rowcount
