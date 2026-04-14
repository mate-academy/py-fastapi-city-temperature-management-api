import httpx

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from city_api.models import City
from temperature_api.models import Temperature
from temperature_api.schemas import TemperatureCreateSchema


WEATHER_API_KEY = "8464599207c1130f6731978501b3f34e"

WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather"


async def create_temperature(data: TemperatureCreateSchema, db: AsyncSession):

    temperature = Temperature(
        date_time=data.date_time,
        temperature=data.temperature,
        city_id=data.city_id
    )

    db.add(temperature)
    await db.commit()
    await db.refresh(temperature)

    return temperature


async def get_temperature(db: AsyncSession):
    request = await db.execute(select(Temperature))
    temperatures = request.scalars().all()

    return temperatures


async def update_temperature(db: AsyncSession):

    request = await db.execute(select(City))
    cities = request.scalars().all()

    async with httpx.AsyncClient() as client:

        for city in cities:

            params = {
                "q": city.name,
                "appid": WEATHER_API_KEY,
                "units": "metric"
            }

            try:
                response = await client.get(WEATHER_URL, params=params)
                response.raise_for_status()

                data = response.json()

                current_temperature = data["main"]["temp"]

                temp_record = Temperature(
                    city_id=city.id,
                    temperature=current_temperature
                )
                db.add(temp_record)
                await db.commit()


            except httpx.HTTPStatusError as e:
                print(f"City with name: {city.name} does not exist: {e.response.status_code}")
            except Exception as e:
                print(f"Other error: {e}")
