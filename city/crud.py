from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from city import schemas
from db import models
from dependencies import PaginationDep


class CityNotFoundError(Exception):
    """City with given id does not exist."""


async def get_all_cities(
    db: AsyncSession,
    pagination: PaginationDep,
) -> Sequence[models.City]:

    db_cities = await db.scalars(
        select(models.City)
        .order_by(models.City.id)
        .offset(pagination.skip)
        .limit(pagination.limit)
    )
    return db_cities.all()


async def get_city(db: AsyncSession, city_id: int) -> models.City | None:

    db_city = await db.scalar(select(models.City).where(models.City.id == city_id))

    if db_city is None:
        raise CityNotFoundError

    return db_city


async def create_city(db: AsyncSession, city: schemas.CityCreate) -> models.City:

    db_city = models.City(
        name=city.name,
        additional_info=city.additional_info,
    )

    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)

    return db_city


async def update_city(
    db: AsyncSession,
    city_id: int,
    city: schemas.CityCreate,
) -> models.City:

    db_city = await get_city(db, city_id)

    db_city.name = city.name
    db_city.additional_info = city.additional_info

    await db.commit()
    await db.refresh(db_city)

    return db_city


async def delete_city(db: AsyncSession, city_id: int) -> None:

    db_city = await get_city(db, city_id)

    await db.delete(db_city)
    await db.commit()
