import os
from typing import Sequence

import httpx
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from city import crud as city_crud
from dependencies import get_db, pagination_params
from temperature import crud, schemas, models

load_dotenv()

router = APIRouter()
weather_api_key = os.getenv("WEATHER_API_KEY")


@router.post("/temperatures/update")
async def get_temperatures_list(db: AsyncSession = Depends(get_db)):
    cities = await city_crud.get_cities_list(db)
    weather_url = "http://api.weatherapi.com/v1/current.json"
    async with httpx.AsyncClient() as client:
        for city in cities:
            params = {"key": weather_api_key, "q": city}
            response = await client.get(weather_url, params=params)
            data = response.json()
            temperature_data = schemas.TemperatureCreateSchema(
                city_id=city.id,
                date_time=data["current"]["last_updated"],
                temperature=data["current"]["temp_c"]
            )
            await crud.create_temperature(db=db, temperature=temperature_data)

        return {"message": "Temp updated"}


@router.get(
    "/temperatures", response_model=list[schemas.TemperatureCitySchema]
)
async def get_temperatures(
        pagination: dict = Depends(pagination_params),
        db: AsyncSession = Depends(get_db)
) -> Sequence[models.Temperature]:
    return await crud.get_temperatures(
        db=db, skip=pagination["skip"], limit=pagination["limit"]
    )


@router.get("/temperatures/{city_id}")
async def get_city_temperatures(
        city_id: int, db: AsyncSession = Depends(get_db)
):
    temperatures = await crud.get_temperatures_by_city_id(db, city_id)
    if not temperatures:
        raise HTTPException(status_code=404, detail="Temperatures not found")
    return temperatures
