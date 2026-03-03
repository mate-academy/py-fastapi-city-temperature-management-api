from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from city.models import City
from temperature.models import Temperature
from temperature.schemas import CityMaxTemperatureSchema, TemperatureBaseSchema


async def get_max_temperature(
        db: AsyncSession
) -> list[CityMaxTemperatureSchema]:
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
        CityMaxTemperatureSchema(
            city_id=row.city_id,
            city_name=row.city_name,
            max_temperature=row.max_temperature
        )
        for row in rows
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
