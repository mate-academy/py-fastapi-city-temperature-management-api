from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert

from . import schemas, models


async def get_all_temperatures(
        db: AsyncSession
) -> list[schemas.Temperature]:
    query = select(models.DBTemperature)
    temperature_list = await db.execute(query)
    return [temperature[0] for temperature in temperature_list.fetchall()]


async def get_temperature_for_city(
        db: AsyncSession, city_id: int
) -> schemas.Temperature:
    query = select(models.DBTemperature).where(
        models.DBTemperature.city_id == city_id
    )
    temperature = await db.execute(query)

    temperature = temperature.fetchone()

    if temperature:
        return temperature[0]


async def update_temperatures(
        db: AsyncSession, temperature: schemas.TemperatureCreate
) -> dict:
    query = (
        insert(models.DBTemperature)
        .values(
            date_time=temperature.date_time,
            temperature=temperature.temperature,
            city_id=temperature.city_id,
        )
        .returning(models.DBTemperature.id)
    )
    result = await db.execute(query)
    await db.commit()
    response = {**temperature.model_dump(), "id": result.all()[0][0]}
    return response
