from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from db import models
from db.models import Temperature
from dependencies import PaginationDep


async def get_all_temperature(
    db: AsyncSession,
    pagination: PaginationDep,
) -> Sequence[Temperature]:

    result = await db.scalars(
        select(models.Temperature)
        .options(selectinload(models.Temperature.city))
        .order_by(models.Temperature.id)
        .offset(pagination.skip)
        .limit(pagination.limit)
    )
    return result.all()


async def get_temperature_by_city_id(
    db: AsyncSession,
    city_id: int,
    pagination: PaginationDep,
) -> Sequence[Temperature]:

    result = await db.scalars(
        select(models.Temperature)
        .options(selectinload(models.Temperature.city))
        .where(models.Temperature.city_id == city_id)
        .order_by(models.Temperature.id)
        .offset(pagination.skip)
        .limit(pagination.limit)
    )
    return result.all()


async def create_temperature(
    db: AsyncSession, city_id: int, value: float
) -> models.Temperature:

    db_temperature = models.Temperature(city_id=city_id, temperature=value)
    db.add(db_temperature)
    await db.commit()
    await db.refresh(db_temperature, attribute_names=["city"])
    return db_temperature
