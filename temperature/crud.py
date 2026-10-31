from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from city.router import cities_get
from temperature import models, schemas


async def get_all_temperatures(db: AsyncSession) -> list[models.Temperature]:
    temperatures = await db.scalars(select(models.Temperature))
    return list(temperatures.all())


async def get_temperature_in_city(db: AsyncSession, city_id: int) -> models.Temperature | None:
    temperatures = await db.scalars(select(models.Temperature).where(models.Temperature.city_id == city_id))
    return temperatures.first()


async def fetch_temperature(db: AsyncSession) -> models.Temperature | None:
    cities = await cities_get(db=db)
    temperatures = []
    for city in cities:
        temperatures.append(await get_temperature_in_city(db=db, city_id=city.id))
