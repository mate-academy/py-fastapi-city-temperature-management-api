from sqlalchemy import select, insert

from city import models, schemas

from sqlalchemy.ext.asyncio import AsyncSession


async def create_city(db: AsyncSession, city: schemas.CityCreate):
    db_city = models.City(**city.model_dump())
    db.add(db_city)
    await db.flush()
    await db.commit()
    await db.refresh(db_city)

    return db_city


async def get_cities(db: AsyncSession):
    query = select(models.City)
    cities = await db.execute(query)
    return [city[0] for city in cities.fetchall()]


async def delete_city(db: AsyncSession, city_id: int):
    query = select(models.City).filter(models.City.id == city_id)
    city = await db.execute(query)
    city = city.scalar()

    if city:
        await db.delete(city)
        await db.commit()

    return {"message": "City deleted successfully"}
