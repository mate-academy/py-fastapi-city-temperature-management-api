from typing import Sequence

from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from city import models, schemas


async def get_all_cities(db: AsyncSession) -> Sequence[models.City]:
    query = select(models.City)
    cities_list = await db.execute(query)

    return cities_list.scalars().all()


async def get_city_by_id(db: AsyncSession, city_id: int) -> models.City:
    query = select(models.City).where(models.City.id == city_id)
    city = await db.execute(query)

    return city.scalar()


async def get_city_by_name(db: AsyncSession, city_name: str) -> models.City:
    query = select(models.City).where(models.City.name == city_name)
    city = await db.execute(query)

    return city.scalar()


async def create_city(db: AsyncSession, city: schemas.CityCreate) -> models.City:
    query = insert(models.City).values(
        name=city.name,
        additional_info=city.additional_info,
    )
    result = await db.execute(query)
    await db.commit()

    created_city = await get_city_by_id(db=db, city_id=result.lastrowid)

    return created_city


async def update_city(
    db: AsyncSession, city_id: int, city: schemas.CityUpdate
) -> models.City:
    query = update(models.City).where(models.City.id == city_id).values(**city.dict())
    await db.execute(query)
    await db.commit()

    updated_city = await get_city_by_id(db=db, city_id=city_id)

    return updated_city


async def delete_city(db: AsyncSession, city_id: int) -> None:
    query = delete(models.City).where(models.City.id == city_id)
    await db.execute(query)
    await db.commit()
