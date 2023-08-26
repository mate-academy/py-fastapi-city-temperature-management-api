from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

import cities.models as models
import cities.schemas as schemas


async def get_all_cities(
        db: AsyncSession,
) -> list[models.City]:
    query = select(models.City)
    city_list = await db.execute(query)
    return [city[0] for city in city_list.fetchall()]


async def get_city(
        db: AsyncSession,
        city_id: int,
) -> [models.City | None]:
    query = select(models.City).where(
        models.City.id == city_id
    )
    city = await db.execute(query)
    city = city.fetchone()

    if city:
        return city[0]

    return None


async def get_city_by_name(
        db: AsyncSession,
        city_name: str,
) -> [models.City | None]:
    query = select(models.City).where(
        models.City.name == city_name
    )
    city = await db.execute(query)
    city = city.fetchone()

    if city:
        return city[0]

    return None


async def create_city(
        db: AsyncSession,
        city: schemas.CityCreate,
) -> dict:
    query = insert(models.City).values(
        name=city.name,
        additional_info=city.additional_info,
    )
    new_city = await db.execute(query)

    await db.commit()

    new_city = {**city.model_dump(), "id": new_city.lastrowid}

    return new_city


async def update_city(
        db: AsyncSession,
        city_id: int,
        new_data: dict,
) -> [models.City | None]:
    query = select(models.City).where(
        models.City.id == city_id
    )
    updated_city = await db.execute(query)
    updated_city = updated_city.fetchone()

    if updated_city:
        updated_city = updated_city[0]

        for field_name, value in new_data.items():
            setattr(updated_city, field_name, value)

        await db.commit()
        await db.refresh(updated_city)

        return updated_city

    return None


async def delete_city(
        db: AsyncSession,
        city_id: int,
) -> [dict | bool]:
    query = select(models.City).where(
        models.City.id == city_id
    )
    deleted_city = await db.execute(query)
    deleted_city = deleted_city.fetchone()

    if deleted_city:
        await db.delete(deleted_city[0])
        await db.commit()

        return {"message": "City deleted"}

    return False
