from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from city import models, schemas


async def create_city(db: AsyncSession, data: schemas.CityCreate) -> models.City:
    city = models.City(**data.model_dump())
    db.add(city)
    await db.commit()
    return city


async def get_all_cities(db: AsyncSession) -> list[models.City]:
    cities = await db.scalars(select(models.City))
    return list(cities.all())


async def get_city_by_id(db: AsyncSession, city_id: int) -> models.City | None:
    return await db.get(models.City, city_id)


async def update_city(
    db: AsyncSession, city_id: int, data: schemas.CityUpdate
) -> models.City | None:
    city = await get_city_by_id(db, city_id)
    if city is None:
        return None
    for field, value in data.model_dump().items():
        setattr(city, field, value)
    await db.commit()
    return city


async def delete_city(db: AsyncSession, city_id: int) -> bool:
    city = await get_city_by_id(db, city_id)
    if city is None:
        return False
    await db.delete(city)
    await db.commit()
    return True
