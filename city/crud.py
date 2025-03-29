from typing import List, Type

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from city import models, schemas
from city.models import City
from utils import get_object_or_404


async def get_list_of_cities(
        db: AsyncSession,
        limit: int,
        offset: int
) -> List[models.City]:
    query = select(models.City).offset(offset).limit(limit)
    cities_list = await db.execute(query)
    return [city[0] for city in cities_list.fetchall()]


async def add_city(db: AsyncSession, city: schemas.CityIn) -> models.City:
    query = insert(models.City).values(
        name=city.name,
        additional_info=city.additional_info,
    )
    result = await db.execute(query)
    await db.commit()

    response = schemas.City(**city.model_dump(), id=result.lastrowid)
    return response


async def get_city(db: AsyncSession, city_id: int) -> Type[models.City]:
    stored_city = await get_object_or_404(db, model=City, obj_id=city_id)
    return stored_city


async def update_city(
        db: AsyncSession,
        city_id: int,
        payload_city: schemas.CityIn
) -> models.City:
    stored_city = await get_object_or_404(db, obj_id=city_id, model=City)

    for key, value in payload_city.items():
        setattr(stored_city, key, value)
    await db.commit()
    await db.refresh(stored_city)

    return stored_city


async def partial_update_city(
        db: AsyncSession,
        city_id: int,
        payload_city: schemas.CityIn
) -> models.City:
    stored_city = await get_object_or_404(db, obj_id=city_id, model=City)

    for key, value in payload_city.model_dump(exclude_unset=True).items():
        setattr(stored_city, key, value)
    await db.commit()
    await db.refresh(stored_city)

    return stored_city


async def delete_city(db: AsyncSession, city_id: int) -> models.City:
    stored_city = await get_object_or_404(db, obj_id=city_id, model=City)
    await db.delete(stored_city)
    await db.commit()
    return stored_city
