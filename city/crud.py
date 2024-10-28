from fastapi import HTTPException

from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession

from city import models, schemas


async def get_all_cities(db: AsyncSession) -> list[models.City]:
    query = select(models.City)
    cities_list = await db.execute(query)

    return [city[0] for city in cities_list.fetchall()]


async def create_city(db: AsyncSession, city: schemas.CityCreate) -> dict:
    query = insert(models.City).values(
        name=city.name,
        additional_info=city.additional_info,
    )
    created_city = await db.execute(query)
    await db.commit()
    response = {**city.model_dump(), "id": created_city.lastrowid}

    return response


async def retrieve_city(db: AsyncSession, id: int) -> models.City:
    city = await db.get(models.City, id)

    return city


async def update_city(
    db: AsyncSession,
    id: int,
    city_data: dict
) -> models.City:
    city = await retrieve_city(db, id)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")

    for key, value in city_data.items():
        if hasattr(city, key):
            setattr(city, key, value)

    await db.commit()
    await db.refresh(city)

    return city


async def delete_city(db: AsyncSession, id: int) -> None:
    existing_city = await db.get(models.City, id)

    if not existing_city:
        raise HTTPException(status_code=404, detail="City not found")

    query = delete(models.City).where(models.City.id == id)

    await db.execute(query)
    await db.commit()
