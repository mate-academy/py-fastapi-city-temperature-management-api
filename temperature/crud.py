from fastapi import HTTPException, status
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from city import models as city_models
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
    city_query = select(city_models.DBCity).where(
        city_models.DBCity.id == temperature.city_id
    )
    result = await db.execute(city_query)
    existing_city = result.fetchone()

    if not existing_city:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="City not found"
        )
    query = insert(models.DBTemperature).values(
        city_id=temperature.city_id,
        date_time=temperature.date_time,
        temperature=temperature.temperature,
    )
    result = await db.execute(query)
    await db.commit()
    resp = {**temperature.model_dump(), "id": result.lastrowid}
    return resp
