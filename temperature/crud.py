import httpx
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
import temperature.models as models
import temperature.schemas as schemas
from city.models import City as city_model
from get_weather import get_weather


async def get_all_temperatures(db: AsyncSession) -> list[models.Temperature]:
    temperatures = db.query(models.Temperature).all()
    return temperatures


async def create_temperature(
        db: AsyncSession, temperature: schemas.TemperatureCreate
) -> models.Temperature:
    db_temperature = models.Temperature(
        city_id=temperature.city_id,
        date_time=temperature.date_time,
        temperature=temperature.temperature,
    )
    db.add(db_temperature)
    await db.commit()
    await db.refresh(db_temperature)

    return db_temperature


async def get_temperature_for_specific_city(
        db: AsyncSession, city_id: int | None = None
) -> models.Temperature | None:
    queryset = db.query(models.Temperature)

    if city_id is not None:
        queryset = queryset.filter(models.Temperature.city_id == city_id)

    return queryset.first()


async def update_all_temperatures_async(db: AsyncSession):
    cities = await db.query(city_model).all()

    async with httpx.AsyncClient() as client:
        tasks = [get_weather(city.name) for city in cities]
        temperatures = await asyncio.gather(*tasks)

    for city, temperature in zip(cities, temperatures):
        city.temperature = temperature

    await db.commit()
