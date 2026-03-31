from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from city import models, schemas


async def get_all_cities(db: AsyncSession) -> list[models.DBCity]:
    cities = await db.scalars(select(models.DBCity))

    return cities.all()


async def get_city_by_name(db: AsyncSession, city_name: str) -> models.DBCity | None:
    return await db.scalar(select(models.DBCity).where(models.DBCity.name == city_name))


async def get_city_by_id(db: AsyncSession, city_id: int) -> models.DBCity | None:
    return await db.scalar(select(models.DBCity).where(models.DBCity.id == city_id))


async def create_city(db: AsyncSession, city: schemas.CityCreate) -> models.DBCity:
    db_city = models.DBCity(name=city.name, additional_info=city.additional_info)
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)

    return db_city


async def delete_city(db: AsyncSession, db_city: models.DBCity):
    await db.delete(db_city)
    await db.commit()


async def update_city(
    db: AsyncSession, db_city: models.DBCity, city_update: schemas.CityCreate
):
    db_city.name = city_update.name
    db_city.additional_info = city_update.additional_info
    await db.commit()
    await db.refresh(db_city)
    return db_city
