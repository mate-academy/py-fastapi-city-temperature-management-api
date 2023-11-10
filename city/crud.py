from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from city import models, schemas


async def create_city(city: schemas.CityCreate, db: AsyncSession):
    query = insert(models.City).values(
        name=city.name, additional_info=city.additional_info
    )
    result = await db.execute(query)
    await db.commit()
    response = {**city.model_dump(), "id": result.lastrowid}
    return response


async def read_cities(db: AsyncSession):
    query = select(models.City)
    cities_list = await db.execute(query)
    return [city[0] for city in cities_list.fetchall()]


async def read_city(city_id: int, db: AsyncSession):
    query = select(models.City).where(models.City.id == city_id)
    result = await db.execute(query)
    city = result.scalar_one_or_none()
    return city


async def update_city(
        city_id: int, city_update: schemas.CityUpdate, db: AsyncSession
):
    query = (
        update(models.City)
        .where(models.City.id == city_id)
        .values(**city_update.dict(exclude_unset=True))
    )
    await db.execute(query)
    await db.commit()


async def delete_city(city_id: int, db: AsyncSession):
    query = delete(models.City).where(models.City.id == city_id)
    result = await db.execute(query)
    await db.commit()
    return result.rowcount
