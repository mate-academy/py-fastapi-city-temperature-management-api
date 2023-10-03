from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from city import models, schemas


async def get_all_cities(db: AsyncSession):
    query = select(models.DBCity)
    result = await db.execute(query)
    return result.scalars().all()


async def get_city(city_id: int, db: AsyncSession):
    query = select(models.DBCity).where(models.DBCity.id == city_id)
    result = await db.execute(query)
    return result.scalar_one()


async def create_city(db: AsyncSession, city: schemas.CityCreate):
    db_city = models.DBCity(
        name=city.name,
        additional_info=city.additional_info
    )
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)
    return db_city


async def update_city(db: AsyncSession,
                      city_id: int,
                      city_update: schemas.CityUpdate) -> models.DBCity:
    db_city = await get_city(db=db, city_id=city_id)
    if db_city:
        for key, value in city_update.model_dump().items():
            setattr(db_city, key, value)
        await db.commit()
        await db.refresh(db_city)
    return db_city


async def delete_city(db: AsyncSession, city_id: int) -> models.DBCity:
    db_city = await get_city(db=db, city_id=city_id)
    if db_city:
        await db.delete(db_city)
        await db.commit()
    return db_city
