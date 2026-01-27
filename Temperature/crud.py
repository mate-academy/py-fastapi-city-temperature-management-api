from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from Temperature.models import Temperature


async def get_temperature(db: AsyncSession, city_id: int):
    return await db.scalar(select(Temperature).where(Temperature.city_id == city_id))

async def get_temperatures(db: AsyncSession):
    query = await db.scalars(select(Temperature))
    return query.all()

async def get_temperatures_by_city(db: AsyncSession, city_id: int):
    query = select(Temperature).where(Temperature.city_id == city_id).order_by(Temperature.date_time.desc())
    result = await db.scalars(query)
    return result.all()

async def create_temperature(db: AsyncSession, city_id: int, temp_val: int):
    db_temp = Temperature(city_id=city_id, temperature=temp_val)
    db.add(db_temp)
    await db.commit()
    await db.refresh(db_temp)
    return db_temp
