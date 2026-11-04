from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from city import models, schemas
from temperature.models import Temperature


async def get_all_cities(
    db: AsyncSession, skip: int = 0, limit: int | None = None
) -> list[models.City]:
    query = select(models.City).offset(skip)
    if limit is not None:
        query = query.limit(limit)
    result = await db.execute(query)
    return list(result.scalars().all())


async def get_city(db: AsyncSession, city_id: int) -> models.City | None:
    return await db.get(models.City, city_id)


async def get_city_by_name(db: AsyncSession, name: str) -> models.City | None:
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
    db: AsyncSession, db_city: models.City, data: schemas.CityCreate
) -> models.City:
    for field, value in data.model_dump().items():
        setattr(db_city, field, value)
    await db.commit()
    await db.refresh(db_city)
    return db_city


async def delete_city(db: AsyncSession, db_city: models.City) -> None:
    await db.execute(
        delete(Temperature).where(Temperature.city_id == db_city.id)
    )
    await db.delete(db_city)
    await db.commit()
