from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.temperature.models import DBTemperature


async def create_temp_record(
        db: AsyncSession, city_id: int, temp: float
) -> DBTemperature:
    async with db:
        temp_entry = DBTemperature(
            city_id=city_id,
            temperature=temp,
            date_time=datetime.utcnow()
        )
        db.add(temp_entry)
        await db.commit()
        await db.refresh(temp_entry)
        return temp_entry


async def get_all_temp(db: AsyncSession) -> [DBTemperature]:
    result = await db.execute(select(DBTemperature))
    temperatures = result.scalars().all()
    return temperatures


async def get_temp_for_city(id_city, db: AsyncSession) -> [DBTemperature]:
    result = select(DBTemperature).where(DBTemperature.city_id == id_city)
    temperatures_city = await db.execute(result)
    return temperatures_city.scalars()
