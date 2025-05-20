from typing import List
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from temperature_app.models import CityModel, TemperatureModel
from temperature_app.schemas import (CityBaseSchema,
                                     TemperatureBaseSchema)


async def create_city_in_db(db: AsyncSession,
                            city_data: CityBaseSchema) -> CityModel:
    db_city = CityModel(name=city_data.name,
                        additional_info=city_data.additional_info)
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)
    return db_city


async def get_single_city_from_db(db: AsyncSession,
                                  city_id: int) -> CityModel:
    db_city = select(CityModel).where(CityModel.id == city_id)
    result = await db.execute(db_city)
    db_city = result.scalar_one_or_none()
    return db_city


async def get_all_cities_from_db(db: AsyncSession) -> List[CityModel]:
    db_cities = select(CityModel)
    result = await db.execute(db_cities)
    db_cities = result.scalars().all()
    return db_cities


async def create_temperature_in_db(
        db: AsyncSession,temperature:
        TemperatureBaseSchema
        ) -> TemperatureModel:
    db_temperature = TemperatureModel(
        city_id=temperature.city_id,
        temperature=temperature.temperature,
        date_time=temperature.date_time
    )
    db.add(db_temperature)
    await db.commit()
    await db.refresh(db_temperature)
    return db_temperature


async def get_temperature_by_city_id_from_db(
        db: AsyncSession, city_id: int
) -> List[TemperatureModel]:
    db_temperatures = select(TemperatureModel).where(
        TemperatureModel.city_id == city_id
    )
    result = await db.execute(db_temperatures)
    db_temperatures = result.scalars().all()
    return [temperature for temperature in db_temperatures]


async def get_temperatures_from_db(
        db: AsyncSession
) -> List[TemperatureModel]:
    db_temperatures = select(TemperatureModel)
    result = await db.execute(db_temperatures)
    db_temperatures = result.scalars().all()
    return [temperature for temperature in db_temperatures]
