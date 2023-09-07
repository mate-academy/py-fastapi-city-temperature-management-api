from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from city import schemas, models


async def create_city(db: AsyncSession, city: schemas.CityCreate):
    db_city = insert(models.City).values(
        name=city.name, additional_info=city.additional_info
    )
    result = await db.execute(db_city)
    await db.commit()
    resp = {**city.model_dump(), "id": result.lastrowid}

    return resp


async def get_all_cities(db: AsyncSession):
    query = select(models.City)
    cities = await db.execute(query)
    cities = cities.fetchall()

    return [city[0] for city in cities]


async def get_city_by_id(db: AsyncSession, id: int):
    query = select(models.City).where(models.City.id == id)

    city = await db.execute(query)
    city = city.fetchone()

    if city:
        return city[0]

    return None


async def delete_city(db: AsyncSession, id: int):
    query = select(models.City).where(models.City.id == id)
    deleted_city = await db.execute(query)
    deleted_city = deleted_city.fetchone()

    if deleted_city:
        await db.delete(deleted_city[0])
        await db.commit()

        return {"message": "City deleted"}

    return False
