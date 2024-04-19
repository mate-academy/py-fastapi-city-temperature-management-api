import os

import httpx
from dotenv import load_dotenv
from fastapi import HTTPException


load_dotenv()

URL = "http://api.weatherapi.com/v1/current.json?"


async def get_temperature(city_name: str) -> tuple:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            url=URL,
            params={"key": os.getenv("WEATHERAPI"), "q": city_name, "aqi": "no"},
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code, detail="Error during fetching"
            )

        response = response.json()

        return city_name, response["current"]["temp_c"]
