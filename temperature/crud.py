from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert

from . import schemas, models


async def create_temperature(
    db: AsyncSession,
    temperature: schemas.TemperatureCreate
):
    query = insert(models.DBTemperature).values(
        date_time=temperature.date_time,
        temperature=temperature.temperature,
        city_id=temperature.city_id,
    ).returning(models.DBTemperature.id)
    result = await db.execute(query)
    await db.commit()
    response = {**temperature.model_dump(), "id": result.all()[0][0]}
    return response


async def get_all_temperature(db: AsyncSession, city_id: int = None):
    query = select(models.DBTemperature)
    if city_id is not None:
        query = query.where(models.DBTemperature.city_id == city_id)
    temp_list = await db.execute(query)
    return [temp[0] for temp in temp_list.fetchall()]
