import os
import httpx

from dotenv import load_dotenv
from fastapi import BackgroundTasks, HTTPException
from sqlalchemy.orm import Session

from city import crud as city_crud
from temperature import crud as temperature_crud
from temperature import models

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = "http://api.weatherapi.com/v1/current.json?"


async def update_temperatures(db: Session):
    cities = city_crud.get_all_cities(db)

    for city in cities:
        city_name = city.name
        city_id = city.id
        temperature = await fetch_temperature(city_name)

        if temperature is not None:
            temperature_model = models.Temperature(city_id=city_id, temperature=temperature)
            temperature_crud.create_temperature(db, temperature_model)


# Function to fetch temperature based on city name using www.weatherapi.com API
async def fetch_temperature(city_name: str) -> int:
    api_url = BASE_URL + f"key={API_KEY}" + "&" + f"q={city_name}"

    async with httpx.AsyncClient() as client:
        response = await client.get(api_url)

    if response.status_code == 200:
        data = response.json()
        temperature = data["current"]["temp_c"]
        return round(temperature)
    else:
        raise HTTPException(
            status_code=400, detail=f"Failed to fetch temperature data for {city_name}. Status code: {response.status_code}"
        )
