import os

import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime
from src.city.models import City as CityModel
from src.exceptions import KeyNotConfigure
from src.temperature.schemas import TemperatureCreate
from src.temperature.crud import create_temperature

OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"


async def fetch_and_update_temperatures(db: AsyncSession) -> None:
    api_key = os.getenv("OPEN_WEATHER_KEY")
    if not api_key:
        raise KeyNotConfigure()

    async with httpx.AsyncClient() as client:
        cities = await db.execute(select(CityModel))
        cities = cities.scalars().all()

        temperature_entries = []

        for city in cities:
            response = await client.get(
                OPENWEATHER_URL,
                params={
                    "q": city.name,
                    "appid": api_key,
                    "units": "metric"
                }
            )
            if response.status_code == 200:
                data = response.json()
                temperature_data = TemperatureCreate(
                    city_id=city.id,
                    date_time=datetime.utcnow(),
                    temperature=data["main"]["temp"]
                )
                temperature_entries.append(temperature_data)
            else:
                print(
                    f"Failed to fetch temperature for "
                    f"{city.name}: {response.status_code} - {response.text}"
                )

        for temperature_data in temperature_entries:
            await create_temperature(db, temperature_data)

        await db.commit()
