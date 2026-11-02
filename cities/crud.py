from typing import List

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from cities import models, schemas


async def get_all_cities(db: AsyncSession) -> List[models.City]:
    cities = await db.scalars(select(models.City))

    return cities.all()

async def create_city(
    db: AsyncSession,
    city: schemas.CityCreate
) -> models.City:
    db_city = models.City(
        **city.model_dump()
    )
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)

    return db_city

async def delete_city(
    db: AsyncSession,
    city_id: int
):
    city = await db.scalar(
        select(models.City).where(models.City.id == city_id)
    )

    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    await db.delete(city)
    await db.commit()

async def get_city_by_name(
    db: AsyncSession,
    name: str
) -> models.City | None:
    return await db.scalar(
        select(
            models.City
        ).where(
            models.City.name == name
        )
    )