from datetime import datetime

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from typing_extensions import List

from city.models import DBCity
from temperature.models import DBTemperature
from temperature.schemas import TemperatureSchema
from temperature.utils import get_city_temperature, api_key, get_city_temperature


async def set_temperature(db: AsyncSession) -> None:
    async with db.begin():
        result = await db.execute(select(DBCity))
        all_city = result.scalars().all()

        for city in all_city:
            temperature = await get_city_temperature(city_name=city.name)

            new_temperature = insert(DBTemperature).values(
                city_id=city.id,
                date_time=datetime.now(),
                temperature=temperature,
            )
            await db.execute(new_temperature)
        await db.commit()


def get_all_temperature(db: Session) -> List[DBTemperature]:
    return db.query(DBTemperature).all()


def get_temperature_for_city(db: Session, city_id: int) -> DBTemperature:
    return db.query(DBTemperature).filter(DBTemperature.city_id == city_id).all()
