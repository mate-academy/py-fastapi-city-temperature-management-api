from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from city.models import DBCity
from city.schemas import CityCreate


async def get_cities_list(db: AsyncSession) -> List[DBCity]:
    query = select(DBCity)
    db_cities = await db.execute(query)

    return list(db_cities.scalars())


async def create_city(db: AsyncSession, city: CityCreate) -> dict:
    query = insert(DBCity).values(
        name=city.name,
        additional_info=city.additional_info,
    )
    result = await db.execute(query)
    await db.commit()
    response = {**city.model_dump(), "id": result.lastrowid}

    return response


async def get_city_by_id(db: AsyncSession, city_id: int) -> int | None:
    query = select(DBCity).where(DBCity.id == city_id)
    city = await db.execute(query)

    return city.scalar()


async def update_city_data(
        db: AsyncSession,
        city_id: int,
        city_data: CityCreate
) -> dict:
    query = (
        update(DBCity).where(DBCity.id == city_id).values(
            name=city_data.name,
            additional_info=city_data.additional_info,
        ).execution_options(synchronize_session="fetch")
    )
    await db.execute(query)
    await db.commit()

    return {f"City with id '{city_id}'": "Updated successfully"}


async def delete_city_data(db: AsyncSession, city_id: int) -> dict:
    query = (
        delete(DBCity).where(
            DBCity.id == city_id
        ).execution_options(synchronize_session="fetch")
    )
    await db.execute(query)
    await db.commit()

    return {f"City with id {city_id}": "Deleted successfully"}
