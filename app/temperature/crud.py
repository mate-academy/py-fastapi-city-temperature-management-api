from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.temperature import models, schemas


async def get_temperatures(
    db: AsyncSession, city_id: int | None = None, skip: int = 0, limit: int = 100
) -> Sequence[models.Temperature]:
    """Retrieves temperature records, optionally filtered by city ID."""
    query = select(models.Temperature)
    if city_id is not None:
        query = query.where(models.Temperature.city_id == city_id)

    fetched_data = await db.scalars(query.offset(skip).limit(limit))

    return fetched_data.all()


async def update_city_temperature(
    db: AsyncSession, temperature_data: schemas.TemperatureCreate
) -> models.Temperature | None:
    """Updates or creates a temperature record for a city."""
    temp = models.Temperature(**temperature_data.model_dump())
    db.add(temp)
    try:
        await db.commit()
        await db.refresh(temp)
        return temp
    except IntegrityError:
        await db.rollback()
        return None
