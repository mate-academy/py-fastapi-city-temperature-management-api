from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.city_app import DBCity, CityCreate, City, CityUpdate


def raise_error(
        status_code: int,
        message: str,
):
    raise HTTPException(
        status_code=status_code,
        detail=f"Endpoint raise exception: {message}"
    )


async def create_new_city(db: AsyncSession, city: CityCreate) -> City:
    db_city = DBCity(**city.model_dump())
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)
    return db_city


async def get_list_of_city(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100,
) -> List[City]:
    result = await db.scalars(
        select(DBCity).offset(skip).limit(limit)
    )
    return result.all()


async def get_city_by_id(
        db: AsyncSession,
        city_id: int
) -> Optional[DBCity]:
    result = await db.get(
        DBCity,
        city_id
    )
    return result


async def update_city(
        db: AsyncSession,
        city_id: int,
        city: CityUpdate
) -> DBCity:
    db_item = await get_city_by_id(db, city_id)
    if not db_item:
        raise_error(404, f"City with id {city_id} not found")

    city_data = city.model_dump(exclude_unset=True)
    for key, value in city_data.items():
        setattr(db_item, key, value)

    await db.commit()
    await db.refresh(db_item)
    return db_item


async def delete_city(
        db: AsyncSession,
        city_id: int
) -> None:
    db_item = await get_city_by_id(db, city_id)
    if not db_item:
        raise_error(404, f"City with id {city_id} not found")

    await db.delete(db_item)
    await db.commit()

    return None