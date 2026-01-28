from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from cities import models
from cities import schemas


async def get_all_cities(db: AsyncSession) -> List[models.City]:
    result = await db.execute(select(models.City))
    return list(result.scalars().all())


async def create_city(db: AsyncSession, city: schemas.CityCreate) -> models.City:
    db_city = models.City(
        name=city.name,
        additional_info=city.additional_info,
        latitude=city.latitude,
        longitude=city.longitude,
    )
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)

    return db_city


async def delete_city(db: AsyncSession, city_id: int) -> bool:
    db_city = await db.scalar(
        select(models.City).where(models.City.id == city_id))
    if db_city:
        await db.delete(db_city)
        await db.commit()
        return True
    return False
