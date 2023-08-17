from sqlalchemy import select, insert, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from temperature import models, schemas


async def get_all_temperatures(db: AsyncSession, city_id: int | None = None):
    query = select(models.DBTemperature)

    if city_id is not None:
        query = query.where(models.DBTemperature.city_id == city_id)

    temperature_list = await db.execute(query)

    return [temperature[0] for temperature in temperature_list.fetchall()]


async def create_temperature(
    db: AsyncSession, temperature: schemas.TemperatureCreate
):
    query = insert(models.DBCity).values(
        city_id=temperature.city_id,
        date_time=temperature.date_time,
        temperature=temperature.temperature,
    )
    result = await db.execute(query)
    await db.commit()
    resp = {**temperature.model_dump(), "id": result.lastrowid}
    return resp
