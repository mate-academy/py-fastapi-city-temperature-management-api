from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

import temperatures.models as models
from sqlalchemy.orm import selectinload


async def get_all_temperatures(
        db: AsyncSession,
        city_id: int | None,
) -> list[models.Temperature]:
    query = select(models.Temperature).options(
        selectinload(models.Temperature.city)
    )

    if city_id:
        query = query.where(models.Temperature.city_id == city_id)

    temperature_list = await db.execute(query)

    return [temperature[0] for temperature in temperature_list.fetchall()]


async def create_temperature(
        db: AsyncSession,
        data: dict,
) -> None:
    query = insert(models.Temperature).values(
        city_id=data["city_id"],
        temperature=data["temperature"],
    )
    await db.execute(query)
