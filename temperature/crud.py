from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from temperature.models import Temperature


async def list_temperatures(db: AsyncSession):
    query = select(Temperature)
    temperature_list = await db.execute(query)

    if temperature_list is not None:
        return [temperature[0] for temperature in temperature_list]
    return []


async def retrieve_temperature(db: AsyncSession, city_id: int):
    query = (
        select(Temperature)
        .where(Temperature.city_id == city_id)
    )
    temperature = await db.execute(query)
    return [temperature[0] for temperature in temperature.fetchall()]


async def create_temperature(db: AsyncSession, data: dict):
    query = insert(Temperature).values(
        temperature=data["temperature"],
        city_id=data["city_id"],
    )

    await db.execute(query)
    await db.commit()
