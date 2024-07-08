from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from city import models, schemas


async def get_all_cities(db: AsyncSession) -> List[models.DBCity]:
    result = await db.execute(select(models.DBCity))
    return result.scalars().all()


async def get_city_by_name(db: AsyncSession, name: str) -> Optional[models.DBCity]:
    result = await db.execute(select(models.DBCity).filter(models.DBCity.name == name))
    return result.scalars().first()


async def create_city(db: AsyncSession, city: schemas.CityCreate) -> models.DBCity:
    db_city = models.DBCity(
        name=city.name,
        additional_info=city.additional_info,
    )
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)
    return db_city


async def get_city(db: AsyncSession, city_id: int) -> Optional[models.DBCity]:
    result = await db.execute(select(models.DBCity).filter(models.DBCity.id == city_id))
    return result.scalars().first()


async def update_city(
    db: AsyncSession, city_id: int, city_update: schemas.CityCreate
) -> Optional[models.DBCity]:
    result = await db.execute(select(models.DBCity).filter(models.DBCity.id == city_id))
    db_city = result.scalars().first()
    if db_city:
        db_city.name = city_update.name
        db_city.additional_info = city_update.additional_info
        await db.commit()
        await db.refresh(db_city)
        return db_city
    return None


async def delete_city(db: AsyncSession, city_id: int) -> Optional[models.DBCity]:
    result = await db.execute(select(models.DBCity).filter(models.DBCity.id == city_id))
    db_city = result.scalars().first()
    if db_city:
        await db.delete(db_city)
        await db.commit()
        return db_city
    return None
