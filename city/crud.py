from typing import Optional, List

from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from . import models, schemas


async def create_city(db: AsyncSession, city_data: schemas.CityCreate) -> models.City:
    query = insert(models.City).values(
        name=city_data.name,
        additional_info=city_data.additional_info
    )

    result = await db.execute(query)
    await db.commit()

    return result.scalar_one()

async def get_city(db: AsyncSession, city_id: int) -> Optional[models.City]:
    result = await db.execute(
        select(models.City).where(models.City.id == city_id)
    )

    return result.scalar_one_or_none()

async def get_all_cities(db: AsyncSession) -> List[models.City]:
    result = await db.execute(select(models.City))

    return [city[0] for city in result.fetchall()]

async def update_city(
        db: AsyncSession,
        city_id: int, city_data: schemas.CityUpdate
) -> Optional[models.City]:
    query = (
        update(models.City)
        .where(models.City.id == city_id)
        .values(
            name=city_data.name,
            additional_info=city_data.additional_info
        )
        .returning(models.City)
    )

    result = await db.execute(query)
    await db.commit()

    return result.scalar_one_or_none()

async def delete_city(db: AsyncSession, city_id: int) -> bool:
    query = delete(models.City).where(models.City.id == city_id)
    result = await db.execute(query)
    await db.commit()

    return result.rowcount() > 0