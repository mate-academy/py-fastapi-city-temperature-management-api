import os
from dotenv import load_dotenv
import httpx
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.session import get_db
from src.schemas import TemperatureCreate, Temperature
from src.database.models.crud import (
    create_temperature,
    get_all_temperatures,
    get_temperatures_by_city,
    get_cities,
)

load_dotenv()

router = APIRouter()

WEATHER_API_URL = (
    "http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city_name}"
)

API_KEY = os.getenv("API_KEY")

if not API_KEY:
    raise ValueError("API key not found in environment variables.")

@router.post("/temperatures/update")
async def update_temperature_view(db: AsyncSession = Depends(get_db)):
    cities = await get_cities(db)

    if not cities:
        raise HTTPException(status_code=404, detail="No cities found in the database.")

    async with httpx.AsyncClient() as client:
        for city in cities:
            url = WEATHER_API_URL.format(API_KEY=API_KEY, city_name=city.name)

            try:
                response = await client.get(url)
                response.raise_for_status()
            except httpx.HTTPStatusError as http_err:
                raise HTTPException(
                    status_code=http_err.response.status_code,
                    detail=f"Error fetching temperature data for {city.name}: {http_err}"
                )
            except httpx.RequestError as req_err:
                raise HTTPException(
                    status_code=503,
                    detail=f"Error connecting to weather service: {req_err}"
                )

            weather_data = response.json()

            try:
                date_time = weather_data["location"]["localtime"]
                temperature = weather_data["current"]["temp_c"]
            except KeyError as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Error parsing weather data for {city.name}: {str(e)}"
                )

            temperature_create = TemperatureCreate(
                city_id=city.id, date_time=date_time, temperature=temperature
            )
            try:
                await create_temperature(db=db, temperature=temperature_create)
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Error saving temperature for {city.name}: {str(e)}"
                )

    return {"message": "Temperature updated successfully for all cities."}


@router.get("/temperatures", response_model=list[Temperature])
async def get_all_temperatures_view(db: AsyncSession = Depends(get_db)):
    temperatures = await get_all_temperatures(db)
    if not temperatures:
        raise HTTPException(status_code=404, detail="No temperature records found")

    return [
        {
            "id": temp.id,
            "city_id": temp.city_id,
            "city": temp.city.name,
            "date_time": temp.date_time,
            "temperature": temp.temperature,
        }
        for temp in temperatures
    ]


@router.get("/temperatures/city", response_model=list[Temperature])
async def get_temperatures_for_city_view(
    city_id: int, db: AsyncSession = Depends(get_db)
):
    if city_id is None:
        raise HTTPException(status_code=400, detail="City ID must be provided")

    temperatures = await get_temperatures_by_city(db, city_id)
    if not temperatures:
        raise HTTPException(
            status_code=404, detail="Temperatures not found for the given city"
        )

    return temperatures
