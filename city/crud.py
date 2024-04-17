
from city.models import City
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import CityCreate
from sqlalchemy import select, insert, update, delete


async def get_all_cities(db: AsyncSession):
    query = select(City)
    cities_list = await db.execute(query)
    return [city[0] for city in cities_list.fetchall()]


async def get_cities_by_name(db: AsyncSession, name: str):
    query = select(City).filter(City.name == name)
    city = await db.execute(query)
    return city.scalar_one_or_none()


async def get_city_by_id(db: AsyncSession, city_id: int):
    query = select(City).filter(City.id == city_id)
    city = await db.execute(query)
    return city.scalar_one_or_none()


async def create_city(db: AsyncSession, city: CityCreate):
    query = insert(City).values(
        name=city.name,
        additional_info=city.additional_info
    )
    result = await db.execute(query)
    await db.commit()
    response = {**city.model_dump(), "id": result.lastrowid}
    return response


async def update_city(db: AsyncSession, city_id: int, city: CityCreate):
    query = update(City).where(City.id == city_id).values(
        name=city.name,
        additional_info=city.additional_info
    )
    await db.execute(query)
    await db.commit()

    return {
        "id": city_id,
        **city.model_dump()
    }


async def delete_city(db: AsyncSession, city_id: int):
    query = delete(City).where(City.id == city_id)
    await db.execute(query)
    await db.commit()
