from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.cities.models import DBCity
from src.cities.schemas import CityCreate


async def get_all_cities(db: AsyncSession) -> list[DBCity]:
    query = select(DBCity)
    city_list = await db.execute(query)
    return [city[0] for city in city_list.fetchall()]


async def create_new_city(
    db: AsyncSession, city: CityCreate
) -> dict[str, int]:
    query = insert(DBCity).values(**city.model_dump())
    result = await db.execute(query)
    await db.commit()
    return {"id": result.lastrowid}


async def delete_city_by_id(db: AsyncSession, city_id: int) -> dict[str, int]:
    query = delete(DBCity).where(DBCity.id == city_id)
    result = await db.execute(query)
    await db.commit()
    return {"id": result.lastrowid}
