from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from . import models, schemas
from typing import List, Optional


async def create_city(db: AsyncSession, city: schemas.CityCreate) -> models.City:
    db_city = models.City(**city.dict())
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)
    return db_city


async def get_city(db: AsyncSession, city_id: int) -> Optional[models.City]:
    result = await db.execute(select(models.City).where(models.City.id == city_id))
    return result.scalars().first()


async def get_cities(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100
) -> List[models.City]:
    result = await db.execute(select(models.City).offset(skip).limit(limit))
    return result.scalars().all()


async def update_city(
    db: AsyncSession,
    city_id: int,
    city_update: schemas.CityCreate
) -> Optional[models.City]:
    result = await db.execute(
        update(models.City)
        .where(models.City.id == city_id)
        .values(**city_update.dict())
        .returning(models.City)
    )
    updated_city = result.scalar_one_or_none()
    if not updated_city:
        return None
    await db.commit()
    return await get_city(db, city_id)


async def delete_city(db: AsyncSession, city_id: int) -> bool:
    existing_city = await get_city(db, city_id)
    if not existing_city:
        return False

    await db.execute(delete(models.City).where(models.City.id == city_id))
    await db.commit()
    return True


async def create_temperature(
        db: AsyncSession,
        temperature: schemas.TemperatureCreate,
        city_id: int
) -> models.Temperature:
    db_temperature = models.Temperature(**temperature.dict(), city_id=city_id)
    db.add(db_temperature)
    await db.commit()
    await db.refresh(db_temperature)
    return db_temperature


async def get_temperatures(
        db: AsyncSession,
        city_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100
) -> List[models.Temperature]:
    query = select(models.Temperature)
    if city_id is not None:
        query = query.where(models.Temperature.city_id == city_id)

    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


async def get_temperature(
        db: AsyncSession,
        temperature_id: int
) -> Optional[models.Temperature]:
    result = await db.execute(
        select(models.Temperature).where(models.Temperature.id == temperature_id)
    )
    return result.scalars().first()


async def delete_temperature(db: AsyncSession, temperature_id: int) -> bool:
    existing_temp = await get_temperature(db, temperature_id)
    if not existing_temp:
        return False

    await db.execute(
        delete(models.Temperature).where(models.Temperature.id == temperature_id)
    )
    await db.commit()
    return True
