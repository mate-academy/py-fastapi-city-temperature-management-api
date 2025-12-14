from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app import models, schemas


async def get_city_list(db: AsyncSession) -> list[models.DBCity]:
    cities = await db.scalars(
        select(models.DBCity)
        .options(selectinload(models.DBCity.temperatures))
    )
    return cities.all()


async def get_city_by_id(
        db: AsyncSession,
        city_id: int
) -> models.DBCity | None:
    return await db.scalar(
        select(models.DBCity).where(models.DBCity.id == city_id)
        .options(selectinload(models.DBCity.temperatures))
    )


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


async def get_city_by_name(
        db: AsyncSession,
        name: str
) -> models.DBCity | None:
    return await db.scalar(
        select(models.DBCity).where(models.DBCity.name == name)
    )


async def get_temperature_list(db: AsyncSession) -> list[models.DBTemperature]:
    db_temperatures = await db.scalars(
        select(models.DBTemperature)
        .options(selectinload(models.DBTemperature.city))
    )
    return db_temperatures.all()


async def get_temperatures_by_city_id(
        db: AsyncSession,
        city_id: int
) -> list[models.DBTemperature]:
    db_temperatures = await db.scalars(
        select(models.DBTemperature)
        .where(models.DBTemperature.city_id == city_id)
        .options(selectinload(models.DBTemperature.city))
    )
    return db_temperatures.all()
