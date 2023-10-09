import httpx

from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from city.models import DBCity

from temperature.models import DBTemperature
from temperature.utils import get_temperature_from_api


async def update_temperatures(db: AsyncSession) -> dict:

    query = select(DBCity)
    cities = await db.execute(query)
    invalid_cities = []

    async with httpx.AsyncClient() as client:
        for city in cities.fetchall():
            try:
                temp_celsius, last_updated = await get_temperature_from_api(
                    city[0].name,
                    client
                )
                temperature = DBTemperature(
                    city_id=city[0].id,
                    temperature=temp_celsius,
                    date_time=last_updated
                )
                db.add(temperature)
            except ValueError:
                invalid_cities.append(city[0].name)

        await db.commit()

    return_message = {
        "message":
            "Temperature data for cities has updated successfully!",
        "invalid_cities":
            "Every city has been processed"
    }
    if invalid_cities:
        return_message["invalid_cities"] = (
            "But we can`t receive current temperature for this cities: "
            f"{[city for city in invalid_cities]}"
        )

    return return_message


async def get_all_temperatures(db: AsyncSession,
                               skip: int,
                               limit: int) -> list:
    query = select(DBTemperature).offset(skip).limit(
        limit
    ).order_by(
        DBTemperature.city_id,
        text("temperatures.date_time DESC")
    )
    temperatures = await db.execute(query)

    return [temperature[0] for temperature in temperatures.fetchall()]


async def get_temperatures_by_city_id(db: AsyncSession,
                                      skip: int,
                                      limit: int,
                                      city_id: int) -> list:
    query = select(DBTemperature).offset(skip).limit(
        limit
    ).filter(
        DBTemperature.city_id==city_id
    ).order_by(text("temperatures.date_time DESC"))

    temperatures = await db.execute(query)

    return [temperature[0] for temperature in temperatures.fetchall()]