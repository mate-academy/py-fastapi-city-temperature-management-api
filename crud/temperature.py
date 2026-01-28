from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.models import DBTemperature
from schemas.temperature import TemperatureCreate, Temperature


async def get_all_temperature_records(db: AsyncSession):
    result = await db.execute(select(DBTemperature))

    return result.scalars().all()

async def get_temperature_for_city(db: AsyncSession, city_id: int):
    result = await db.execute(
        select(DBTemperature).where(DBTemperature.city_id == city_id)
    )
    return result.scalars().all()

async def create_temperature_record(db: AsyncSession, city_id: int, temp_value: float):
    new_record = DBTemperature(
        city_id=city_id,
        temperature=temp_value,
        date_time=datetime.now()
    )
    db.add(new_record)

