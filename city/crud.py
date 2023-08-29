from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from . import schemas, models


async def list_cities(db: AsyncSession):
    query = select(models.City)
    cities_list = await db.execute(query)
    return [city[0] for city in cities_list.fetchall()]


async def retrieve_city(db: AsyncSession, city_id: int):
    query = select(models.City).where(models.City.id == city_id)
    result = await db.execute(query)
    city = result.scalar()
    return city


async def get_city_by_name(db: AsyncSession, city_name: str):
    query = select(models.City).where(models.City.name == city_name)
    result = await db.execute(query)
    city = result.scalar()
    return city


async def create_city(db: AsyncSession, city: schemas.CityCreate):
    query = insert(models.City).values(
        name=city.name,
        additional_info=city.additional_info,
    )
    new_city = await db.execute(query)

    await db.commit()

    new_city = {**city.model_dump(), "id": new_city.lastrowid}

    return new_city


async def update_city(db: AsyncSession, city_id: int, city: dict):
    query = select(models.City).where(models.City.id == city_id)
    updated_city = await db.execute(query)
    updated_city = updated_city.fetchone()

    if updated_city:
        updated_city = updated_city[0]

        for field_name, value in city.items():
            setattr(updated_city, field_name, value)

        await db.commit()
        await db.refresh(updated_city)

        return updated_city

    return None


async def delete_city(db: AsyncSession, city_id: int,):
    query = select(models.City).where(models.City.id == city_id)
    deleted_city = await db.execute(query)
    deleted_city = deleted_city.fetchone()

    if deleted_city:
        await db.delete(deleted_city[0])
        await db.commit()

        return {"message": "City deleted"}

    return False
