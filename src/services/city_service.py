from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.city import City
from src.schemas.city import CityCreate, CityUpdate


async def create_city(db: AsyncSession, payload: CityCreate) -> City:
    new_city = City(**payload.model_dump())
    db.add(new_city)
    await db.commit()
    await db.refresh(new_city)
    return new_city


async def get_cities(db: AsyncSession) -> Sequence[City]:
    cities = await db.scalars(select(City))
    return cities.all()


async def get_city_by_id(city_id: int, db: AsyncSession) -> City:
    city = await db.scalar(select(City).where(City.id == city_id))
    return city


async def update_city(city_id, payload: CityUpdate, db: AsyncSession) -> City | None:
    city = await get_city_by_id(city_id=city_id, db=db)
    if not city:
        return None

    city_data = payload.model_dump(exclude_unset=True)
    for key, value in city_data.items():
        setattr(city, key, value)
    await db.commit()
    await db.refresh(city)
    return city


async def delete_city(city_id: int, db: AsyncSession) -> bool:
    city = await get_city_by_id(city_id=city_id, db=db)
    if not city:
        return False
    await db.delete(city)
    await db.commit()
    return True
