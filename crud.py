from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List
from datetime import datetime
import models
import schemas


# City CRUD operations
async def get_city(db: AsyncSession, city_id: int) -> Optional[models.City]:
    result = await db.execute(
        select(models.City).where(models.City.id == city_id)
    )
    return result.scalar_one_or_none()


async def get_city_by_name(
    db: AsyncSession, name: str
) -> Optional[models.City]:
    result = await db.execute(
        select(models.City).where(models.City.name == name)
    )
    return result.scalar_one_or_none()


async def get_cities(
    db: AsyncSession, skip: int = 0, limit: int = 100
) -> List[models.City]:
    result = await db.execute(select(models.City).offset(skip).limit(limit))
    return result.scalars().all()


async def create_city(
    db: AsyncSession, city: schemas.CityCreate
) -> models.City:
    db_city = models.City(name=city.name, additional_info=city.additional_info)
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)
    return db_city


async def update_city(
    db: AsyncSession, city_id: int, city_update: schemas.CityUpdate
) -> Optional[models.City]:
    db_city = await get_city(db, city_id)
    if not db_city:
        return None

    update_data = city_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_city, field, value)

    await db.commit()
    await db.refresh(db_city)
    return db_city


async def delete_city(db: AsyncSession, city_id: int) -> bool:
    db_city = await get_city(db, city_id)
    if not db_city:
        return False

    await db.delete(db_city)
    await db.commit()
    return True


# Temperature CRUD operations
async def create_temperature(
    db: AsyncSession, temperature: schemas.TemperatureCreate
) -> models.Temperature:
    db_temp = models.Temperature(
        city_id=temperature.city_id,
        temperature=temperature.temperature,
        date_time=temperature.date_time or datetime.utcnow(),
    )
    db.add(db_temp)
    await db.commit()
    await db.refresh(db_temp)
    return db_temp


async def get_temperatures(
    db: AsyncSession,
    city_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100
):
    query = select(models.Temperature)
    if city_id:
        query = query.where(models.Temperature.city_id == city_id)
    query = (
        query.offset(skip).limit(limit).order_by(
            models.Temperature.date_time.desc()
        )
    )
    result = await db.execute(query)
    return result.scalars().all()


async def get_temperatures_with_cities(
    db: AsyncSession, city_id: Optional[int] = None
):
    from sqlalchemy.orm import selectinload

    query = select(models.Temperature).options(
        selectinload(models.Temperature.city)
    )
    if city_id:
        query = query.where(models.Temperature.city_id == city_id)
    query = query.order_by(models.Temperature.date_time.desc())
    result = await db.execute(query)
    return result.scalars().all()
