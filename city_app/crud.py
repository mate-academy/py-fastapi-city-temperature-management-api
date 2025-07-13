from typing import Sequence

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from . import models
from . import schemas


async def get_all_cities(db: AsyncSession) -> Sequence[models.City]:
    return (await db.scalars(select(models.City))).all()


async def create_city(db: AsyncSession, city: schemas.CityDtoCreate) -> models.City:
    new_city = models.City(**city.model_dump())
    db.add(new_city)
    await db.commit()
    await db.refresh(new_city)
    return new_city


async def delete_city(db: AsyncSession, city_id: int) -> None:
    user = await db.get(models.City, city_id)
    if user:
        await db.delete(user)
        await db.commit()


async def get_all_temperatures(db: AsyncSession) -> Sequence[models.Temperature]:
    stmt = select(models.Temperature).options(selectinload(models.Temperature.city))
    return (await db.scalars(stmt)).all()


async def get_temperature_by_city(db: AsyncSession, city_id: int) -> Sequence[models.Temperature]:
    stmt = (select(models.Temperature)
            .options(selectinload(models.Temperature.city))
            .where(models.Temperature.city_id == city_id))
    return (await db.scalars(stmt)).all()


async def create_temperature(db: AsyncSession, temperature: schemas.TemperatureDtoCreate) -> models.Temperature:
    new_temperature = models.Temperature(**temperature.model_dump())
    db.add(new_temperature)
    await db.commit()
    await db.refresh(new_temperature)

    stmt = (
        select(models.Temperature)
        .options(selectinload(models.Temperature.city))
        .where(models.Temperature.id == new_temperature.id)
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()