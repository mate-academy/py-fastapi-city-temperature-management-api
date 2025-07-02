from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from cities import schemas, models


async def create_city(db: AsyncSession, city: schemas.CityCreate) -> models.City:
    new_city = models.City(**city.model_dump())
    db.add(new_city)

    try:
        await db.commit()
        await db.refresh(new_city)
    except IntegrityError:
        await db.rollback()
        raise

    return new_city


async def get_city_by_id(db: AsyncSession, city_id: int) -> models.City | None:
    stmt = select(models.City).where(models.City.id == city_id)
    result = await db.execute(stmt)
    city = result.scalar_one_or_none()

    return city


async def get_all_cities(db: AsyncSession) -> list[models.City]:
    stmt = select(models.City)
    result = await db.execute(stmt)
    cities = result.scalars().all()

    return cities


async def update_city(
    db: AsyncSession, city_id, city_update: schemas.CityUpdate
) -> models.City | None:
    city = await get_city_by_id(db, city_id)

    if city is None:
        return None

    update_data = city_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(city, key, value)

    await db.commit()
    await db.refresh(city)
    return city


async def delete_city(db: AsyncSession, city_id: int) -> bool | None:
    city = await get_city_by_id(db, city_id)

    if city is None:
        return None

    await db.delete(city)
    await db.commit()

    return True
