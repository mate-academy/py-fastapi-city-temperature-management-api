from typing import Any

from sqlalchemy import CursorResult
from sqlalchemy.ext.asyncio import AsyncSession

from city_temp_app import schemas


async def create_temperature(
        db: AsyncSession, temperature: schemas.Temperature
) -> dict[str, CursorResult[Any]]:
    query = insert(models.Temperature).values(
        name=temperature.name,
        additional_info=temperature.additional_info
    )
    last_record_id = await db.execute(query)
    return {**temperature.dict(), "id": last_record_id}


async def read_temperatures(
        db: AsyncSession, city_id: Optional[int] = None
) -> Sequence[Temperature]:
    query = select(models.Temperature)
    if city_id:
        query = select(models.Temperature).filter(
            models.Temperature.id == city_id
        )

    result = await db.execute(query)
    return result.scalars().all()
