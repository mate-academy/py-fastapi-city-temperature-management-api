from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from temperature import schemas, models


async def get_all_temperatures(db: AsyncSession, city_id: int | None):
    query = select(models.Temperature).options(selectinload(models.Temperature.city))

    if city_id is not None:
        query = query.filter(models.Temperature.city.has(id=city_id))

    result = await db.execute(query)
    return result.scalars().all()


async def create_temperature(temperature: schemas.TemperatureCreate, db: AsyncSession):
    temperature_data = temperature.model_dump()
    query = insert(models.Temperature).values(**temperature_data)
    result = await db.execute(query)
    await db.commit()
    resp = {**temperature.model_dump(), "id": result.lastrowid}
    return resp
