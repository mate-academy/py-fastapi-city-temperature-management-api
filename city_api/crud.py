from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert
from city_api import models, schemas


async def create_city(db: AsyncSession, city: schemas.CityCreate):
    query = insert(models.City).values(
        name=city.name,
        additional_info=city.additional_info,
    )
    result = await db.execute(query)
    await db.commit()
    resp = {**city.model_dump(), "id": result.lastrowid}
    return resp


async def get_city(db: AsyncSession, city_id: int) -> models.City:
    query = select(models.City).filter(models.City.id == city_id)
    city = await db.execute(query)
    return city.scalar()


async def delete_city(db: AsyncSession, city_id: int):
    db_city = await get_city(db, city_id)
    await db.delete(db_city)
    await db.commit()
    return {"message": "City deleted"}


async def get_cities(db: AsyncSession):
    query = select(models.City)
    cities = await db.execute(query)
    return [city[0] for city in cities.fetchall()]
