from fastapi import HTTPException
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from city import models, schemas


async def get_all_cities(db: AsyncSession) -> list[models.City]:
    query = select(models.City)
    result = await db.execute(query)
    return result.scalars().all()


async def create_city(db: AsyncSession, city: schemas.CityCreate) -> dict:
    query = insert(models.City).values(
        name=city.name,
        additional_info=city.additional_info,
    ).returning(models.City.id)
    result = await db.execute(query)
    created_city_id = result.scalar_one()
    await db.commit()
    return {**city.model_dump(), "id": created_city_id}


async def retrieve_city(db: AsyncSession, id: int) -> models.City:
    city = await db.get(models.City, id)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found.")
    return city


async def update_city(db: AsyncSession, id: int,
                      city_data: dict) -> models.City:
    city = await retrieve_city(db, id)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found.")

    for key, value in city_data.items():
        if hasattr(city, key) and getattr(city, key) != value:
            setattr(city, key, value)

    await db.commit()
    await db.refresh(city)
    return city


async def delete_city(db: AsyncSession, id: int) -> None:
    city = await retrieve_city(db, id)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found.")

    await db.delete(city)
    await db.commit()
