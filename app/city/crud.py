from collections.abc import Sequence
from typing import TypeVar

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.city import models, schemas

T = TypeVar("T", schemas.CityCreate, schemas.CityUpdate)


async def get_cities(
    db: AsyncSession, skip: int = 0, limit: int | None = 100
) -> Sequence[models.City]:
    """Retrieves a list of cities from the database."""

    query = select(models.City)
    if limit is not None:
        query = query.offset(skip).limit(limit)

    fetched_data = await db.scalars(query)

    return fetched_data.all()


async def get_city_by_id(db: AsyncSession, city_id: int) -> models.City | None:
    """Retrieves a city by its ID from the database."""
    fetched_data = await db.get(models.City, city_id)

    return fetched_data


async def _catch_integrity_error(db: AsyncSession, city: models.City) -> None:
    try:
        await db.commit()
        await db.refresh(city)

    except IntegrityError:
        await db.rollback()

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"City with the name '{city.name}' already exists.",
        )


def check_city_existence(city_id: int, city: models.City | None) -> None:
    """Checks if a city exists and raises HTTPException if not."""
    if not city:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"City with the id '{city_id}' does not exist.",
        )


async def create_city(db: AsyncSession, city_data: schemas.CityCreate) -> models.City:
    """Creates a new city in the database."""
    new_city = models.City(**city_data.model_dump())
    db.add(new_city)
    await _catch_integrity_error(db, city=new_city)

    return new_city


async def update_city(
    db: AsyncSession, city_id: int, update_data: schemas.CityUpdate
) -> models.City:
    """Updates an existing city in the database."""
    check_city_existence(
        city_id=city_id, city=(db_city := await get_city_by_id(db, city_id=city_id))
    )

    for key, value in update_data.model_dump(exclude_unset=True).items():
        setattr(db_city, key, value)

    await _catch_integrity_error(db, city=db_city)

    return db_city


async def delete_city(db: AsyncSession, city_id: int) -> None:
    """Deletes a city from the database."""
    check_city_existence(
        city_id=city_id, city=(db_city := await get_city_by_id(db, city_id=city_id))
    )

    await db.delete(db_city)
    await db.commit()

    return None
