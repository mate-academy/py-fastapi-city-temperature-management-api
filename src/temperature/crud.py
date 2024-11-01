import os
from typing import Optional
from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from datetime import datetime
from sqlalchemy.future import select
import httpx
from src.temperature.models import Temperature
from src.city.models import City

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("WEATHER_API_KEY")
URL = os.getenv("BASE_URL")


async def update_temperature(db: AsyncSession):
    result = await db.execute(select(City))
    cities = result.scalars().all()

    temperatures = []

    async with httpx.AsyncClient() as client:
        for city in cities:
            params = {
                "key": API_KEY,
                "q": city.name
            }
            response = await client.get(URL, params=params)

            if response.status_code == 200:
                print("WE WERE HERE !!!!!")
                data = response.json()

                temperature = data["current"]["temp_c"]

                new_temp = Temperature(
                    city_id=city.id,
                    date_time=datetime.now(),
                    temperature=temperature
                )

                temperatures.append(new_temp)
            else:
                print(
                    f"Error fetching data for city {city.name}: "
                    f"{response.json().get('error', {}).get(
                        'message', 'Unknown error'
                    )}"
                )

    for temp in temperatures:
        db.add(temp)

    await db.commit()

    for temp in temperatures:
        await db.refresh(temp)

    return temperatures


async def get_temperature(db: AsyncSession, city_id: Optional[int]):
    query = select(Temperature).filter(
        Temperature.city_id == city_id
    ) if city_id else select(Temperature)
    result = await db.execute(query)
    temperatures = result.scalars().all()

    if city_id is not None and not temperatures:
        raise HTTPException(
            status_code=404,
            detail=f"Temperature records for city_id {city_id} not found."
        )

    return temperatures


async def get_specific_city_temperature(db: AsyncSession, city_id):
    result = await db.execute(
        select(Temperature).filter(Temperature.city_id == city_id)
    )
    temperatures = result.scalars().all()
    return temperatures
