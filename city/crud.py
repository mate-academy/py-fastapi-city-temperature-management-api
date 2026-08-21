from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from city import schemas, models


async def get_cities(
    db: AsyncSession, skip: int = 0, limit: int | None = None
) -> list[models.City]:
    stmt = select(models.City).order_by(models.City.id).offset(skip)
    if limit is not None:
        stmt = stmt.limit(limit)
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def get_city(db: AsyncSession, city_id: int) -> models.City | None:
    return await db.get(models.City, city_id)


async def create_city(db: AsyncSession, data: schemas.CityCreate) -> models.City:
    city = models.City(**data.model_dump())
    db.add(city)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise
    await db.refresh(city)
    return city


async def update_city(
    db: AsyncSession, city: models.City, data: schemas.CityUpdate
) -> models.City:
    for key, value in data.model_dump(exclude_unset=True, exclude_none=True).items():
        setattr(city, key, value)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise
    return city


async def delete_city(db: AsyncSession, city: models.City) -> None:
    await db.delete(city)
    await db.commit()
