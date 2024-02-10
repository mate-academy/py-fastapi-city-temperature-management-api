from typing import Optional

from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from city import schemas
from city.models import City


async def get_all_cities(db: AsyncSession) -> list[City]:
    query = select(City)
    city_list = await db.execute(query)

    return [city[0] for city in city_list.fetchall()]


async def get_city_by_id(
        db: AsyncSession,
        city_id: int
) -> Optional[City]:
    query = select(City).where(City.id == city_id)
    result = await db.execute(query)
    city = result.scalars().first()

    return city


async def create_city(
        db: AsyncSession,
        city: schemas.CityCreate
) -> dict[str, int]:
    query = insert(City).values(
        name=city.name,
        additional_info=city.additional_info
    )
    result = await db.execute(query)
    await db.commit()
    response = {**city.model_dump(), "id": result.lastrowid}

    return response


async def update_city(
        db: AsyncSession,
        city_id: int,
        city: dict
) -> Optional[City]:
    query = update(City).where(City.id == city_id).values(**city)
    await db.execute(query)
    await db.commit()
    query = select(City).where(City.id == city_id)
    result = await db.execute(query)
    updated_city = result.scalars().first()

    return updated_city


async def delete_city(
        db: AsyncSession,
        city_id: int
) -> dict:
    query = delete(City).where(City.id == city_id)
    await db.execute(query)
    await db.commit()

    return {"detail": f"City with ID: {city_id} - deleted."}
