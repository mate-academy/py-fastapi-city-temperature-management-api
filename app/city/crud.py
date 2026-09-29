from typing import List, Optional, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.city import models, schemas


async def get_cities(
    db: AsyncSession, skip: int = 0, limit: int = 100
) -> Sequence[models.City]:
    result = await db.execute(
        select(models.City).order_by(models.City.id).offset(skip).limit(limit)
    )
    return result.scalars().all()


async def get_all_cities(db: AsyncSession) -> List[models.City]:
    result = await db.execute(select(models.City).order_by(models.City.id))
    return list(result.scalars().all())


async def get_city(db: AsyncSession, city_id: int) -> Optional[models.City]:
    return await db.get(models.City, city_id)


async def get_city_by_name(
    db: AsyncSession, name: str
) -> Optional[models.City]:
    result = await db.execute(
        select(models.City).where(models.City.name == name)
    )
    return result.scalar_one_or_none()


async def create_city(
    db: AsyncSession, city: schemas.CityCreate
) -> models.City:
    db_city = models.City(**city.model_dump())
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)
    return db_city


async def update_city(
    db: AsyncSession, db_city: models.City, city: schemas.CityUpdate
) -> models.City:
    for field, value in city.model_dump(exclude_unset=True).items():
        setattr(db_city, field, value)
    await db.commit()
    await db.refresh(db_city)
    return db_city


async def delete_city(db: AsyncSession, db_city: models.City) -> None:
    await db.delete(db_city)
    await db.commit()
