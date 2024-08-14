from sqlalchemy import update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from city import models, schemas


async def get_city_by_id(
        db: AsyncSession, city_id: int
) -> models.City | None:
    result = await db.execute(
        select(models.City).filter(models.City.id == city_id)
    )
    return result.scalar_one_or_none()


async def get_city_by_name(
        db: AsyncSession, name: str
) -> models.City | None:
    result = await db.execute(
        select(models.City).filter(models.City.name == name)
    )
    return result.scalar_one_or_none()


async def get_cities(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 10
) -> list[models.City]:
    result = await db.execute(
        select(models.City).offset(skip).limit(limit))
    return result.scalars().all()


async def create_city(
        db: AsyncSession,
        city: schemas.CityCreate
) -> models.City:
    db_city = models.City(
        name=city.name, additional_info=city.additional_info
    )
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)
    return db_city


async def delete_city(
        db: AsyncSession, city_id: int
) -> None:
    await db.execute(
        delete(models.City).where(models.City.id == city_id)
    )
    await db.commit()


async def update_city(
        db: AsyncSession,
        city_id: int,
        city_update: schemas.CityUpdate
) -> models.City | None:
    result = await db.execute(
        update(models.City)
        .where(models.City.id == city_id)
        .values(
            name=city_update.name, additional_info=city_update.additional_info
        )
        .returning(models.City)
    )
    updated_city = result.scalar_one_or_none()
    if updated_city:
        await db.commit()
    return updated_city
