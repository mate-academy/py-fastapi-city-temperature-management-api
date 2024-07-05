from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from cities import models
from cities import schemas
from typing import List


async def get_all_cities(db: AsyncSession) -> List[models.DBCity]:
    query = select(models.DBCity)
    result = await db.execute(query)
    return result.scalars().all()


async def get_city_by_name(db: AsyncSession, name: str) -> models.DBCity:
    query = select(models.DBCity).filter(models.DBCity.name == name)
    result = await db.execute(query)
    return result.scalars().first()


async def create_city(
        db: AsyncSession, city: schemas.CityCreate
) -> models.DBCity:
    db_city = models.DBCity(
        name=city.name,
        additional_info=city.additional_info,
    )
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)
    return db_city


async def delete_city(db: AsyncSession, city_id: int) -> int:
    result = await db.execute(
        delete(models.DBCity).where(models.DBCity.id == city_id)
    )
    await db.commit()
    return result.rowcount
