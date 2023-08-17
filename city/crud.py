from sqlalchemy import select, insert, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from city import models, schemas


async def get_all_cities(db: AsyncSession):
    query = select(models.DBCity)
    cities_list = await db.execute(query)

    return [city[0] for city in cities_list.fetchall()]


async def get_single_city(db: AsyncSession, city_id: int):
    query = select(models.DBCity).where(models.DBCity.id == city_id)
    result = await db.execute(query)
    city = result.fetchone()

    if city is None:
        return None

    return city[0]


async def create_city(db: AsyncSession, city: schemas.CityCreate):
    query = insert(models.DBCity).values(
        name=city.name, additional_info=city.additional_info
    )
    result = await db.execute(query)
    await db.commit()
    resp = {**city.model_dump(), "id": result.lastrowid}
    return resp


async def update_city(
    db: AsyncSession, city_id: int, city: schemas.CityCreate
):
    query = (
        update(models.DBCity)
        .where(models.DBCity.id == city_id)
        .values(
            name=city.name,
            additional_info=city.additional_info,
        )
    )
    result = await db.execute(query)
    await db.commit()
    return result.rowcount > 0


async def delete_city(db: AsyncSession, city_id: int):
    query = delete(models.DBCity).where(models.DBCity.id == city_id)
    result = await db.execute(query)
    await db.commit()
    return result.rowcount > 0
