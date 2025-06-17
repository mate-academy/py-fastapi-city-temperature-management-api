from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession

from . import models, schemas


async def get_cities(db: AsyncSession):
    query = select(models.DBCity)
    result = await db.execute(query)
    cities = result.scalars().all()
    return cities


async def create_city(
       db: AsyncSession,
       city: schemas.CityCreate
):
    query = insert(models.DBCity).values(
        name=city.name,
        additional_info=city.additional_info
    )
    result = await db.execute(query)
    await db.commit()
    resp = {**city.model_dump(), "id": result.lastrowid}
    return resp


async def get_city(db: AsyncSession, city_id: int):
    query = select(models.DBCity).where(models.DBCity.id == city_id)
    resp = await db.execute(query)
    return resp.scalar_one_or_none()


async def get_city_by_name(db: AsyncSession, name: str):
    query = select(models.DBCity).where(models.DBCity.name == name)
    resp = await db.execute(query)
    return resp.scalar_one_or_none()


async def update_city(db: AsyncSession, city_id: int, city_data: schemas.CityUpdate):
    query = (
        update(models.DBCity)
        .where(models.DBCity.id == city_id)
        .values(
            name=city_data.name,
            additional_info=city_data.additional_info
        )
        .execution_options(synchronize_session="fetch")
    )
    await db.execute(query)
    await db.commit()
    return await get_city(db, city_id)


async def delete_city(db: AsyncSession, city_id: int):
    city = await get_city(db, city_id)
    if city:
        await db.delete(city)
        await db.commit()
        return True
    return False
