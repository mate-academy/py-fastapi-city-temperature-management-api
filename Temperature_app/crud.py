from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from sqlalchemy.orm import selectinload

from Temperature_app.models import DBTemperature


class TemperaturesGetter:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.stmt = (
        select(DBTemperature)
        .options(selectinload(DBTemperature.city))
        .order_by(desc(DBTemperature.date_time))
    )

    def set_filter_by_city_id(self, city_id: int) -> None:
        self.stmt = self.stmt.where(DBTemperature.city_id == city_id)

    async def get_result(self) -> List[DBTemperature]:
        temperatures = await self.db.scalars(self.stmt)
        return list(temperatures)


async def get_all_temperatures(db: AsyncSession) -> List[DBTemperature]:
    temperatures_getter = TemperaturesGetter(db=db)
    return await temperatures_getter.get_result()


async def get_temperature_by_city_id(
    db: AsyncSession,
    city_id: int
) -> List[DBTemperature]:
    temperatures_getter = TemperaturesGetter(db=db)
    temperatures_getter.set_filter_by_city_id(city_id)
    return await temperatures_getter.get_result()


async def create_temperature(
        db: AsyncSession,
        temperature_data: dict
) -> DBTemperature:
    temperature = DBTemperature(
        city_id=temperature_data.get("city_id"),
        temperature=temperature_data.get("temperature")
    )
    db.add(temperature)

    await db.commit()
    await db.refresh(temperature)

    return temperature
