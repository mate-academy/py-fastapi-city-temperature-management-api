from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.temperature import Temperature
from app.models.city import City
from datetime import datetime

async def create_temperature(db: AsyncSession, city_id: int, temp: float):
    temp_record = Temperature(city_id=city_id, temperature=temp, date_time=datetime.utcnow())
    db.add(temp_record)
    await db.commit()
    await db.refresh(temp_record)
    return temp_record

async def get_all_temperatures(db: AsyncSession):
    result = await db.execute(select(Temperature))
    return result.scalars().all()

async def get_city_temperatures(db: AsyncSession, city_id: int):
    result = await db.execute(select(Temperature).where(Temperature.city_id == city_id))
    return result.scalars().all()
