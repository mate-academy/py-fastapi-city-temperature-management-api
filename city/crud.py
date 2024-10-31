from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from city import models, schemas


async def get_all_cities(db: AsyncSession):
    query = select(models.City)
    result = await db.execute(query)
    return result.scalars().all()


async def get_city_by_id(db: AsyncSession, city_id: int):
    query = select(models.City).where(models.City.id == city_id)
    city = await db.execute(query)
    return city.scalar_one_or_none()


async def create_city(db: AsyncSession, city: schemas.CityCreate):
    query = insert(models.City).values(city.model_dump())
    result = await db.execute(query)
    await db.commit()
    resp = {**city.model_dump(), "id": result.lastrowid}
    return resp


async def update_city(db: AsyncSession, city_id: int, city: schemas.CityUpdate):
    query = (
        update(models.City)
        .where(models.City.id == city_id)
        .values(city.model_dump())
        .execution_options(synchronize_session="fetch")
    )
    result = await db.execute(query)

    if result.rowcount == 0:
        return None

    query = select(models.City).where(models.City.id == city_id)
    city = await db.execute(query)
    return city.scalar_one_or_none()


async def delete_city(db: AsyncSession, city_id: int):
    query = delete(models.City).where(models.City.id == city_id)
    result = await db.execute(query)

    if result.rowcount == 0:
        return None

    await db.commit()
    return True
