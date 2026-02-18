from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from temperature.models import Temperature


async def async_create_temperatures(
    db: AsyncSession,
    temperatures: list[Temperature],
) -> list[Temperature]:

    db.add_all(temperatures)
    await db.commit()

    for temperature in temperatures:
        await db.refresh(temperature)

    return temperatures


async def async_get_temperatures(
    db: AsyncSession, city_id: int | None = None
) -> list[Temperature]:

    queryset = select(Temperature)

    if city_id is not None:
        queryset = queryset.where(Temperature.city_id == city_id)

    temperatures = await db.scalars(queryset)

    return temperatures.all()
