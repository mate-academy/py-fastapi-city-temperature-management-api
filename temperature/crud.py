from sqlalchemy.ext.asyncio import AsyncSession
from temperature import models, weather, schemas
from city import models as city_models
from sqlalchemy import select, insert


async def get_temperatures(db: AsyncSession):
    query = select(models.Temperature)
    temperatures = await db.execute(query)
    return [temperature[0] for temperature in temperatures.fetchall()]


async def get_city_temperature(db: AsyncSession, city_id: int):
    query = select(models.Temperature).filter(models.Temperature.city_id == city_id)
    temperatures = await db.execute(query)
    return [temperature[0] for temperature in temperatures.fetchall()]


async def update_temperatures(db: AsyncSession):
    cities = await db.execute(select(city_models.City))

    for city in cities.scalars():
        temperature = await weather.get_weather(city.name)

        new_temperature = models.Temperature(city_id=city.id, temperature=temperature)
        db.add(new_temperature)

    await db.commit()
