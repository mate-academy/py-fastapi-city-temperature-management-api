from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert
from sqlalchemy.orm import selectinload

from . import models, schemas
from datetime import datetime, timezone


async def get_all_temperatures(
    db: AsyncSession,
    city_id: int | None = None,
):
    query = select(models.Temperature).options(selectinload(models.Temperature.city))
    if city_id:
        query = query.filter(models.Temperature.city_id == city_id)
    temperatures_list = await db.execute(query)
    return [item[0] for item in temperatures_list.fetchall()]


async def create_new_item_temperature(
    db: AsyncSession,
    city_id: int,
    temperature: float
):
    query = insert(models.Temperature).values(
        city_id=city_id,
        date_time=datetime.now(timezone.utc),
        temperature=temperature
    ).returning(models.Temperature.id)
    
    result = await db.execute(query)
    await db.commit()
    new_id = result.fetchone()[0]
    temperature_item = await db.get(models.Temperature, new_id)
    await db.refresh(temperature_item)
    response = schemas.Temperature.model_validate(temperature_item)
    return response
