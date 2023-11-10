from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from temperature import schemas, models


async def create_temperature_record(
        temperature_data: schemas.TemperatureCreate, db: AsyncSession
):
    query = insert(models.Temperature).values(
        city_id=temperature_data.city_id,
        date_time=temperature_data.date_time,
        temperature=temperature_data.temperature
    )
    result = await db.execute(query)
    await db.commit()
    response = {**temperature_data.model_dump(), "id": result.lastrowid}
    return response


async def get_temperatures(db: AsyncSession):
    query = select(models.Temperature)
    result = await db.execute(query)
    return result.scalars().all()


async def get_temperature_by_id(city_id: int, db: AsyncSession):
    query = select(models.Temperature).where(
        models.Temperature.city_id == city_id
    )
    result = await db.execute(query)
    return result.scalars().all()
