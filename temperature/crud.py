from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from city.crud import get_all_cities
from temperature import models, schemas
from temperature.weather import get_weather


async def get_all_temperatures(
        db: AsyncSession,
        city_id: int
) -> [models.DBTemperature]:
    query = select(models.DBTemperature)
    if city_id is not None:
        query = query.where(models.DBTemperature.city_id == city_id)
    temperatures_list = await db.execute(query)
    return [temperature[0] for temperature in temperatures_list.fetchall()]


async def create_temperature(
        db: AsyncSession,
        temperature: schemas.TemperatureIn,
) -> None:
    query = insert(models.DBTemperature).values(**temperature.model_dump())

    await db.execute(query)


async def update_all_temperatures(db: AsyncSession) -> None:
    cities = await get_all_cities(db=db)
    for city in cities:
        temperatures = await get_all_temperatures(db=db, city_id=city.id)
        if temperatures:
            for temperature in temperatures:
                await db.delete(temperature)
        temperature_in_city = await get_weather(city.name)
        if temperature_in_city == "This city is wrong":
            continue
        temperature_data = schemas.TemperatureIn(
            city_id=city.id,
            temperature=temperature_in_city,

        )
        await create_temperature(db=db, temperature=temperature_data)
    await db.commit()
