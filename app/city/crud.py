from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete

from app.city.models import City
from app.city.schemas import CityCreate, CityUpdate


async def get_all_cities(db: AsyncSession) -> list[City]:
    queryset = select(City)
    city_list = await db.execute(queryset)

    return [city[0] for city in city_list.fetchall()]


async def get_city(db: AsyncSession, city_id: int) -> City | None:
    queryset = select(City).where(City.id == city_id)
    city_list = await db.execute(queryset)
    return city_list.scalar_one_or_none()


async def get_city_by_name(db: AsyncSession, city_name: str) -> City | None:
    queryset = select(City).where(City.name == city_name)
    city_list = await db.execute(queryset)
    return city_list.scalar_one_or_none()


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
