from sqlalchemy import select, Sequence
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from city_api import models, schemas


async def get_all_cities(db: AsyncSession) -> Sequence[models.City]:
    db_cities = await db.scalars(select(models.City))
    return db_cities.all()


async def get_city_by_id(db: AsyncSession, city_id: int) -> models.City | None:
    return await db.scalar(
        select(models.City).where(models.City.id == city_id)
    )


async def get_city_by_name(db: AsyncSession, city_name: str) -> models.City | None:
    return await db.scalar(
        select(models.City).where(models.City.name == city_name)
    )


async def create_city(db: AsyncSession, city: schemas.CityCreate) -> models.City:
    db_city = models.City(**city.model_dump())
    db.add(db_city)

    try:
        await db.commit()
    except IntegrityError as exc:
        await db.rollback()
        raise ValueError(f"City {city.name} already exists") from exc

    await db.refresh(db_city)
    return db_city


async def update_city(
        db: AsyncSession,
        db_city: models.City,
        city_update: schemas.CityUpdate,
):
    update_data = city_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_city, field, value)

    try:
        await db.commit()
    except IntegrityError as exc:
        await db.rollback()
        raise ValueError(f"City {db_city.name} already exists") from exc

    await db.refresh(db_city)
    return db_city


async def delete_city(db: AsyncSession, db_city: models.City) -> None:
    await db.delete(db_city)
    await db.commit()
