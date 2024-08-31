from typing import Type

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from utils import get_or_404
from . import models, schemas
from .models import City


async def get_all_cities(db: AsyncSession, limit: int, offset: int) -> list[models.City]:
    query = select(models.City).limit(limit).offset(offset)
    cities_list = await db.execute(query)
    return [city[0] for city in cities_list.fetchall()]


async def create_city(db: AsyncSession, city: schemas.CityIn) -> models.City:
    query = insert(models.City).values(
        name=city.name,
        additional_info=city.additional_info,
    )
    result = await db.execute(query)
    await db.commit()

    response = schemas.City(**city.model_dump(), id=result.lastrowid)
    return response


async def get_city(db: AsyncSession, city_id: int) -> Type[models.City]:
    stored_city = await get_or_404(db, model=City, obj_id=city_id)
    return stored_city


async def update_city(db: AsyncSession, city_id: int, payload_city: schemas.CityIn) -> models.City:
    stored_city = await get_or_404(db, model=City, obj_id=city_id)

    for key, value in payload_city.model_dump().items():
        setattr(stored_city, key, value)
    await db.commit()
    await db.refresh(stored_city)

    return stored_city


async def partial_update_city(db: AsyncSession, city_id: int, payload_city: schemas.CityPatch) -> models.City:
    stored_city = await get_or_404(db, model=City, obj_id=city_id)

    for key, value in payload_city.model_dump(exclude_unset=True).items():
        setattr(stored_city, key, value)
    await db.commit()
    await db.refresh(stored_city)

    return stored_city


async def delete_city(db: AsyncSession, city_id: int) -> models.City:
    stored_city = await get_or_404(db, model=City, obj_id=city_id)

    await db.delete(stored_city)
    await db.commit()

    return stored_city
