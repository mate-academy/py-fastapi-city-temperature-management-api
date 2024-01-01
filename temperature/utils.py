import os
import httpx

from dotenv import load_dotenv
from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

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
            temperature_model = models.Temperature(
                city_id=city_id,
                temperature=temperature
            )
            temperature_crud.create_temperature(db, temperature_model)


# Function to fetch temperature based on city name using www.weatherapi.com API
async def fetch_temperature(city_name: str) -> int | None:
    api_url = BASE_URL + f"key={API_KEY}" + "&" + f"q={city_name}"

    async with httpx.AsyncClient() as client:
        response = await client.get(api_url)

    if response.status_code == 200:
        data = response.json()
        temperature = data["current"]["temp_c"]
        return round(temperature)
    else:
        error_message = (
            f"Failed to fetch temperature data for {city_name}. "
            f"Status code: {response.status_code}"
        )
        print(error_message)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error_message
        )
