from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from cities import models, schemas


async def create_city(
    db: AsyncSession,
    city: schemas.CityCreate
) -> models.City:
    db_city = models.City(name=city.name, additional_info=city.additional_info)
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)
    return db_city


async def get_cities(db: AsyncSession) -> list[models.City]:
    result = await db.execute(select(models.City))
    return result.scalars().all()


async def get_city(db: AsyncSession, city_id: int) -> models.City | None:
    result = await db.execute(
        select(models.City).filter(models.City.id == city_id)
    )
    return result.scalar_one_or_none()


async def update_city(
    db: AsyncSession,
    city_id: int,
    city: schemas.CityCreate
) -> models.City | None:
    result = await db.execute(
        select(models.City).filter(models.City.id == city_id)
    )
    db_city = result.scalar_one_or_none()
    if db_city:
        db_city.name = city.name
        db_city.additional_info = city.additional_info
        await db.commit()
        await db.refresh(db_city)
    return db_city


async def delete_city(db: AsyncSession, city_id: int) -> bool:
    result = await db.execute(
        select(models.City).filter(models.City.id == city_id)
    )
    db_city = result.scalar_one_or_none()
    if db_city:
        await db.delete(db_city)
        await db.commit()
        return True
    return False
