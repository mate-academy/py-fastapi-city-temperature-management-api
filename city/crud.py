from typing import Optional, List

from sqlalchemy import delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from city import models, schemas


async def get_city(
        db: AsyncSession,
        city_id: int
) -> Optional[models.City]:
    result = await db.execute(
        select(models.City).filter(models.City.id == city_id)
    )
    return result.scalars().first()


async def get_cities(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 10
) -> List[models.City]:
    result = await db.execute(
        select(models.City).offset(skip).limit(limit)
    )
    return result.scalars().all()


async def create_city(
        db: AsyncSession,
        city: schemas.CityCreate
) -> models.City:
    db_city = (
        models.City
        (
            name=city.name,
            additional_info=city.additional_info
        )
    )
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)
    return db_city


async def delete_city(db: AsyncSession, city_id: int) -> None:
    await db.execute(
        delete(models.City).where(models.City.id == city_id)
    )
    await db.commit()


async def update_city(
        db: AsyncSession,
        city_id: int, city:
        schemas.CityUpdate
) -> int:
    result = await db.execute(
        update(models.City)
        .where(models.City.id == city_id)
        .values(name=city.name, additional_info=city.additional_info)
        .execution_options(synchronize_session="fetch")
    )
    await db.commit()
    return result.rowcount
