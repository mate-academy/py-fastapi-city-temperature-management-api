from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from temperature import schemas
import models

async def create_temperature(db: AsyncSession, temp: schemas.TemperatureCreate):
    db_temp = models.Temperature(**temp.dict())
    db.add(db_temp)
    await db.commit()
    await db.refresh(db_temp)
    return db_temp

async def get_all_temperatures(db: AsyncSession):
    result = await db.execute(select(models.Temperature))
    return result.scalars().all()

async def get_temperatures_by_city(db: AsyncSession, city_id: int):
    result = await db.execute(select(models.Temperature).where(models.Temperature.city_id == city_id))
    return result.scalars().all()