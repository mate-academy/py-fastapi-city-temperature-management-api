from sqlalchemy import select, insert, Result
from sqlalchemy.ext.asyncio import AsyncSession

from cities import models, schemas


async def get_cities_list(db: AsyncSession) -> list:
    query = select(models.City)
    cities = await db.execute(query)
    city_list = [city[0] for city in cities.fetchall()]
    return city_list


async def get_city(db: AsyncSession, city_id: int) -> Result:
    query = select(models.City).where(models.City.id == city_id)
    city = await db.execute(query)
    return city.scalar()


async def create_city(
        db: AsyncSession,
        city: schemas.CreateCity
) -> dict:
    city_create = insert(models.City).values(
        name=city.name,
        additional_info=city.additional_info,
    )
    db_city = await db.execute(city_create)
    await db.commit()
    response = {**city.model_dump(), "id": db_city.lastrowid}
    return response


async def update_city(
        db: AsyncSession, city_id: int, new_city_data: schemas.CityBase
) -> Result | None:
    db_city = await get_city(db, city_id)

    if not db_city:
        return None
    for attr, value in new_city_data.model_dump().items():
        setattr(db_city, attr, value)

    await db.commit()
    await db.refresh(db_city)

    return db_city


async def delete_city(db: AsyncSession, city_id: int) -> Result | None:
    db_city = await get_city(db, city_id)
    if not db_city:
        return None
    await db.delete(db_city)
    await db.commit()
    return db_city
