from sqlalchemy import insert
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Any, Optional
from src.temperature.models import Temperature as TemperatureModel
from src.temperature.schemas import TemperatureCreate


async def create_temperature(
    db: AsyncSession,
    temperature: TemperatureCreate
) -> dict[str, Any]:
    query = insert(TemperatureModel).values(
        city_id=temperature.city_id,
        date_time=temperature.date_time,
        temperature=temperature.temperature
    ).returning(TemperatureModel.id)
    result = await db.execute(query)
    await db.commit()
    resp = {**temperature.model_dump(), "id": result.lastrowid}
    return resp


async def get_temperatures(
        db: AsyncSession,
        city_id: Optional[int] = None
) -> List[TemperatureModel]:
    query = select(TemperatureModel)
    if city_id is not None:
        query = query.where(TemperatureModel.city_id == city_id)

    temperature_list = await db.execute(query)
    return [temp[0] for temp in temperature_list.fetchall()]
