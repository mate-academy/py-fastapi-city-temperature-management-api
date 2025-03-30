import httpx
import os
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from fastapi.params import Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from starlette import status
from typing import List, Annotated
from datetime import datetime

from schemes.temperature import TemperatureDetailSchema
from src.database.models import TemperatureModel, CityModel
from database.sqlite_session import get_db


load_dotenv()

router = APIRouter()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
WEATHER_API_URL = os.getenv("WEATHER_API_URL")

DB = Annotated[AsyncSession, Depends(get_db)]


async def get_temperature(city: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            WEATHER_API_URL + f"?q={city}&key={WEATHER_API_KEY}"
        )
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.json().get("message")
            )
        return response.json()


@router.get(
    "/",
    response_model=List[TemperatureDetailSchema],
    status_code=status.HTTP_200_OK,
)
async def get_list_of_temperature(
        db: DB,
        city_id: Annotated[int, Query(ge=0)] = None,
):
    temps_stmt = select(TemperatureModel).options(
        selectinload(TemperatureModel.city)
    )

    if city_id:
        temps_stmt = temps_stmt.where(TemperatureModel.city_id == city_id)

    temps_result = await db.execute(temps_stmt)
    temps = temps_result.scalars().all()

    if not temps:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Temperatures not found."
        )
    return temps


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
async def update_temperature(
        db: DB
):
    cities_stmt = select(CityModel)
    cities_result = await db.execute(cities_stmt)
    cities = cities_result.scalars().all()

    if not cities:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No cities found."
        )

    for city in cities:
        data = await get_temperature(city.name)
        date_time = data["current"].get("last_updated")
        temp = float(data["current"].get("temp_c"))

        temperature = TemperatureModel(
            city_id=city.id,
            date_time=datetime.strptime(date_time, "%Y-%m-%d %H:%M"),
            temperature=temp,
        )
        db.add(temperature)

    await db.commit()

    return {
        "message": "The temperatures were successfully updated."
    }
