from typing import List, Optional

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from city.models import CityModel
from temperature.models import TemperatureModel


async def create_new_city(
    db: AsyncSession,
    name: str,
    info: str,
    temperature: float = 0.0,
) -> CityModel:
    city = CityModel(name=name, additional_info=info)
    db.add(city)
    temperature_model = TemperatureModel(city=city, temperature=temperature)
    db.add(temperature_model)

    await db.commit()
    await db.refresh(city)
    return city


async def get_cities(db: AsyncSession) -> List[CityModel]:
    query = select(CityModel)
    cities = await db.execute(query)
    return cities.scalars().all()


async def get_city(db: AsyncSession, city_id: int) -> Optional[CityModel]:
    query = select(CityModel).where(CityModel.id == city_id)
    city = await db.execute(query)
    return city.scalar_one_or_none()


async def update_city(
    db: AsyncSession, city_id: int, name: str, info: str
) -> Optional[CityModel]:
    query = select(CityModel).where(CityModel.id == city_id)
    result = await db.execute(query)
    city = result.scalar_one_or_none()
    if city is None:
        return None

    city.name = name
    city.additional_info = info

    await db.commit()
    await db.refresh(city)
    return city


async def delete_city(db: AsyncSession, city_id: int) -> None:
    query = delete(CityModel).where(CityModel.id == city_id)
    await db.execute(query)
    await db.commit()
