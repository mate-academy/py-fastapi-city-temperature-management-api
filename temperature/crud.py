from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from temperature.models import Temperature
from temperature.schemas import TemperatureBaseSchema


async def get_all_temperatures_crud(
        db: AsyncSession
) -> list[TemperatureBaseSchema]:
    result = await db.execute(
        select(Temperature)
        .order_by(Temperature.date_time.desc())
    )
    temperatures = result.scalars().all()

    return [
        TemperatureBaseSchema(
            id=t.id,
            city_id=t.city_id,
            temperature=t.temperature,
            date_time=t.date_time
        )
        for t in temperatures
    ]


async def get_max_temperature_for_city(
        db: AsyncSession,
        city_id: int
) -> list[TemperatureBaseSchema]:
    from city.crud import get_cities_by_city_id
    city = await get_cities_by_city_id(db=db, city_id=city_id)

    query = await db.execute(
        select(Temperature)
        .where(Temperature.city_id == city.id)
        .order_by(Temperature.date_time.desc())
    )
    temperatures = query.scalars().all()

    return [
        TemperatureBaseSchema(
            id=t.id,
            city_id=t.city_id,
            temperature=t.temperature,
            date_time=t.date_time
        )
        for t in temperatures
    ]
