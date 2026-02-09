from typing import Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from cities import schemas, models
from cities.models import City


async def get_cities(db: AsyncSession) -> Sequence[models.City]:
    cities = await db.scalars(select(models.City))
    return cities.all()


async def get_city_by_id(db: AsyncSession, city_id: int) -> models.City | None:
    return await db.scalar(select(models.City).where(
        models.City.id == city_id
    ))


async def create_city(
        db: AsyncSession, city: schemas.CityCreate
) -> models.City:
    db_city = models.City(**city.model_dump(exclude_unset=True))
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)
    return db_city


async def update_city(
        db: AsyncSession, data: schemas.CityUpdate, city_id: int
) -> City | None:
    city_db = await get_city_by_id(db=db, city_id=city_id)

    if not city_db:
        return None

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(city_db, field, value)

    await db.commit()
    await db.refresh(city_db)
    return city_db


async def delete_city(db: AsyncSession, city_id: int) -> models.City | None:
    city_db = await get_city_by_id(db, city_id)
    if not city_db:
        return None
    await db.delete(city_db)
    await db.commit()
    return city_db
