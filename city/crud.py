from fastapi import HTTPException
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from city import models
from city import schemas


async def get_all_cities(db: AsyncSession) -> [models.DBCity]:
    result = await db.execute(select(models.DBCity))
    return result.scalars().all()


async def create_city(
        db: AsyncSession,
        city: schemas.CityCreate,
) -> models.DBCity:
    db_city = models.DBCity(
        name=city.name,
        additional_info=city.additional_info,
    )
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)

    return db_city


async def get_city_by_id(
        db: AsyncSession,
        city_id: int,
) -> models.DBCity:
    result = await db.execute(
        select(models.DBCity).filter(models.DBCity.id == city_id)
    )
    return result.scalars().first()


async def delete_city(db: AsyncSession, city_id: int) -> None:
    result = await db.execute(select(models.DBCity)
                              .where(models.DBCity.id == city_id))
    city = result.scalar_one_or_none()

    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    await db.delete(city)
    await db.commit()


async def update_city(
        db: AsyncSession,
        city_id: int,
        city_update_data: schemas.CityUpdate,
) -> models.DBCity:
    result = await db.execute(select(models.DBCity)
                              .where(models.DBCity.id == city_id))
    city = result.scalar_one_or_none()

    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    for key, value in city_update_data.model_dump(exclude_unset=True).items():
        setattr(city, key, value)

    await db.commit()
    await db.refresh(city)

    return city
