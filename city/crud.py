from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from city import models, schemas


async def get_cities(db: AsyncSession) -> list[models.DBCity]:
    cities = await db.scalars(select(models.DBCity))

    return cities.all()


async def get_city_by_id(
    db: AsyncSession, city_id: int
) -> models.DBCity | None:
    return await db.scalar(
        select(models.DBCity).where(models.DBCity.id == city_id)
    )


async def get_city_by_name(
    db: AsyncSession, name: str
) -> models.DBCity | None:
    return await db.scalar(
        select(models.DBCity).where(models.DBCity.name == name)
    )


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


async def delete_city(db: AsyncSession, city: models.DBCity) -> None:
    db_city = await get_city_by_id(db, city.id)
    if db_city:
        await db.delete(db_city)
        await db.commit()
