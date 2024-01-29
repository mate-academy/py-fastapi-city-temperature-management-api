from typing import Sequence

from fastapi import HTTPException
from sqlalchemy import select, update, CursorResult
from sqlalchemy.ext.asyncio import AsyncSession

from city import models
from city import schemas


async def create_city(
        db: AsyncSession,
        city: schemas.CityCreate
) -> models.City:
    new_city = models.City(**city.model_dump())
    db.add(new_city)
    await db.commit()
    await db.refresh(new_city)
    return new_city


async def get_all_city(db: AsyncSession) -> Sequence[models.City]:
    result = await db.execute(select(models.City))  # type: ignore
    return result.scalars().all()


async def check_city(db: AsyncSession, city_id: int) -> CursorResult:
    result = await db.execute(
        select(models.City).where(  # type: ignore
            models.City.id == city_id))
    if result is None:
        raise HTTPException(status_code=404, detail="City not found")
    return result


async def get_city_by_id(db: AsyncSession, city_id: int) -> models.City | None:
    result = await check_city(db, city_id)
    return result.scalar()


async def get_city_by_name(
        db: AsyncSession,
        city_name: str
) -> Sequence[models.City]:
    result = await db.execute(
        select(models.City).where(  # type: ignore
            models.City.name == city_name)
    )
    return result.scalar()


async def update_city(
        db: AsyncSession,
        city: schemas.CityUpdate,
        city_id: int
) -> None:
    up_city = await get_city_by_id(db, city_id)
    query = update(up_city).values(city.model_dump())
    await db.execute(query)
    await db.commit()


async def delete_city(db: AsyncSession, city_id: int) -> None:
    del_city = await check_city(db, city_id)
    await db.delete(del_city)
    await db.commit()
