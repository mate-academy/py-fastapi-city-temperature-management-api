import os

import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from city import crud as city_crud
from temperature import crud as temperature_crud
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
URL = "http://api.weatherapi.com/v1/current.json"


async def fetch_temperature_data(city_name: str):
    params = {
        "key": API_KEY,
        "q": city_name
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(URL, params=params)

        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to fetch temperature data")

        response_data = response.json()
        current_weather = response_data["current"]
        temp_c = current_weather["temp_c"]
        return temp_c


async def update_temperatures(db: AsyncSession):
    cities = await city_crud.get_all_cities(db=db)
    for city in cities:
        temperature = await fetch_temperature_data(city_name=city.name)
        await temperature_crud.update_temperatures_from_api(db=db, city_id=city.id, temperature=temperature)

    return {"message": "Temperature data updated for all cities"}
