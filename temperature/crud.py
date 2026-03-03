from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from city.crud import get_cities_by_city_id
from city.models import City
from temperature.models import Temperature
from temperature.schemas import TemperatureBaseSchema


async def get_max_temperature(db: AsyncSession) -> list[TemperatureBaseSchema]:
    result = await db.execute(
        select(
            City.id.label("city_id"),
            City.name.label("city_name"),
            func.max(Temperature.temperature).label("max_temperature")
        )
        .join(Temperature, City.id == Temperature.city_id)
        .group_by(City.id, City.name)
        .order_by(City.name)
    )

    rows = result.all()
    return [
        TemperatureBaseSchema(
            city_id=row.city_id,
            city_name=row.city_name,
            max_temperature=row.max_temperature
        )
        for row in rows
    ]


async def get_max_temperature_for_city(
        db: AsyncSession,
        city_id: int
) -> float | None:
    city = await get_cities_by_city_id(db=db, city_id=city_id)

    query = await db.execute(
        select(func.max(Temperature.temperature))
        .where(Temperature.city_id == city.id)
    )
    result = query.scalar_one_or_none()

    return result
