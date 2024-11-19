import os

from fastapi import HTTPException
import httpx
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")


async def fetch_temperature(city_name: str) -> float:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://weather.visualcrossing.com/VisualCrossingWebServices/"
            f"rest/services/timeline/{city_name}?unitGroup=metric&include"
            f"=current&key={SECRET_KEY}&contentType=json"
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Error fetching temperature "
                       f"for {city_name}: {response.text}"
            )

        try:
            data = response.json()
            current_conditions = data.get("currentConditions", {})
            return current_conditions.get("temp")
        except ValueError:
            raise HTTPException(
                status_code=500,
                detail="Error parsing JSON response"
            )
