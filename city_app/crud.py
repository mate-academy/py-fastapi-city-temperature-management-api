from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from city_app import models, schemas


async def get_cities_list(db: AsyncSession) -> list[schemas.City]:
    result = await db.scalars(select(models.City))
    return result.all()


async def get_city(db: AsyncSession, city_id) -> schemas.City:
    return await db.scalar(
        select(models.City).where(models.City.id == city_id)
    )


async def create_city(
    db: AsyncSession, city: schemas.CityCreate
) -> schemas.City:
    db_city = models.City(**city.dict())

    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)

    return db_city


async def delete_city(db: AsyncSession, db_city: models.City) -> None:
    await db.delete(db_city)
    await db.commit()


async def update_city(
    db: AsyncSession,
    city_to_update: models.City,
    updated_data: schemas.CityUpdate,
):
    update_data = updated_data.dict(exclude_unset=True)

    for key, value in update_data.items():
        if hasattr(city_to_update, key):
            setattr(city_to_update, key, value)

    await db.commit()
    await db.refresh(city_to_update)
    return city_to_update
