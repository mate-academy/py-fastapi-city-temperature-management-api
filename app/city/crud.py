from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.city import schemas, models


async def create_city(
        db: AsyncSession,
        city: schemas.CityCreate
) -> models.DBCity:
    db_city = models.DBCity(
        name=city.name,
        additional_info=city.additional_info
    )
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)

    return db_city


async def get_cities(db: AsyncSession) -> list[models.DBCity]:
    cities = await db.execute(select(models.DBCity))

    return cities.scalars().all()


async def get_city_by_id(
        db: AsyncSession,
        city_id: int
) -> models.DBCity | None:
    city = await db.execute(
        select(models.DBCity)
        .where(models.DBCity.id == city_id)
    )
    return city.scalar_one_or_none()


async def get_city_by_name(
        db: AsyncSession,
        city_name: str
) -> models.DBCity | None:
    city = await db.execute(
        select(models.DBCity)
        .where(models.DBCity.name == city_name)
    )
    return city.scalar_one_or_none()


async def update_city(
        db: AsyncSession,
        city_id: int,
        city: schemas.CityUpdate
) -> models.DBCity | None:
    db_city = await get_city_by_id(db, city_id)
    if not db_city:
        return None
    db_city.additional_info = city.additional_info
    await db.commit()
    await db.refresh(db_city)

    return db_city


async def delete_city(
        db: AsyncSession,
        city_id: int
) -> models.DBCity | None:
    db_city = await get_city_by_id(db, city_id)
    if db_city:
        await db.delete(db_city)
        await db.commit()
    return db_city
