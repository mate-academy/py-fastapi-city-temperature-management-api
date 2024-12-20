from datetime import datetime

import httpx
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from City_CRUD_API.models import City
from Temperature_API import models
from Temperature_API.models import Temperature
from Temperature_API.schemas import TemperatureCreate


WEATHER_API_URL = "http://api.weatherapi.com/v1/current.json"
API_KEY = "d0eae92abc5b4efaa76144848242007"


async def get_all_temperatures(db: AsyncSession):
    result = await db.execute(select(models.Temperature))
    return result.scalars().all()


async def get_temperature_by_city(db: AsyncSession, city_id: int):
    result = await db.execute(
        select(models.Temperature).
        filter(models.Temperature.city_id == city_id)
    )
    return result.scalars().first()


async def update_temperatures(db: AsyncSession):
    # Get list of all cities
    result = await db.execute(select(City))
    cities = result.scalars().all()

    async with httpx.AsyncClient() as client:
        for city in cities:
            try:
                # Async request to weather API
                response = await client.get(
                    WEATHER_API_URL,
                    params={"key": API_KEY, "q": city.name}
                )

                if response.status_code == 200:
                    data = response.json()
                    temp = data["current"]["temp_c"]  # Temp in JSON response

                    # Create a new record in database
                    db_temp = Temperature(
                        date_time=datetime.utcnow(),
                        temperature=temp,
                        city_id=city.id
                    )
                    db.add(db_temp)
                else:
                    print(
                        f"Not possible to get data for the city"
                        f"{city.name}: {response.status_code}"
                    )
            except Exception as e:
                print(
                    f"Error during getting data for the city {city.name}: {e}"
                )

    # One commit after handling of all cities
    await db.commit()
    return {"message": "Temperatures updated successfully"}


async def create_temperature(
        db: AsyncSession,
        temperatures: TemperatureCreate
):
    db_temp = Temperature(
        date_time=temperatures.date_time,
        temperature=temperatures.temperature,
    )
    db.add(db_temp)
    await db.commit()
    await db.refresh(db_temp)

    return db_temp


async def get_temperature_by_id(db: AsyncSession, temp_id: int):
    result = await db.execute(
        select(models.Temperature).
        filter(models.Temperature.id == temp_id)
    )
    return result.scalars().first()
