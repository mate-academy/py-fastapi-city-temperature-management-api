from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete, Row

from app.city.models import City
from app.city.schemas import CityCreate, CityUpdate


async def get_all_cities(db: AsyncSession) -> list[City]:
    queryset = select(City)
    city_list = await db.execute(queryset)

    return [city[0] for city in city_list.fetchall()]


async def get_city(db: AsyncSession, city_id: int) -> Row[City] | None:
    queryset = select(City).where(City.id == city_id)
    city_list = await db.execute(queryset)
    return city_list.fetchone()


async def get_city_by_name(db: AsyncSession, city_name: str) -> Row[City] | None:
    queryset = select(City).where(City.name == city_name)
    result = await db.execute(queryset)
    city = result.fetchone()

    return city


async def create_city(db: AsyncSession, city_data: CityCreate) -> dict:
    queryset = insert(City).values(**city_data.model_dump())
    result = await db.execute(queryset)

    await db.commit()

    return {**city_data.model_dump(), "id": result.lastrowid}


async def update_city(
    db: AsyncSession,
    city_data: CityUpdate,
    city_id: int
) -> dict:
    queryset = update(City).where(City.id == city_id).values(
        **city_data.model_dump()
    )
    result = await db.execute(queryset)

    await db.commit()

    return {**city_data.model_dump(), "id": result.lastrowid}


async def delete_city(
    db: AsyncSession,
    city_id: int
) -> None:
    queryset = delete(City).where(City.id == city_id)

    await db.execute(queryset)
    await db.commit()
