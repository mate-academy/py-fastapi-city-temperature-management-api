from fastapi import HTTPException
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from city import models
from city import schemas
from city.schemas import CityCreate


async def get_city(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(models.DBCity))
    return result.scalars().all()


async def create_city(db: AsyncSession, city: CityCreate):
    db_city = models.DBCity(
        name=city.name,
        info=city.info,
    )
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)
    return db_city


async def delete_city(db: AsyncSession, city_id: int) -> None:
    result = await db.execute(select(models.DBCity)
                              .where(models.DBCity.id == city_id))
    city = result.scalar_one_or_none()

    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    await db.delete(city)
    await db.commit()
