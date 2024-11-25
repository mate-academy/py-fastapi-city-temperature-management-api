import asyncio
import httpx
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from dotenv import load_dotenv

from settings import settings
from dependencies import get_db
from city.crud import get_city_list
from city.models import City
from temperature import crud, schemas


load_dotenv()

WEATHER_API_URL = "http://api.weatherapi.com/v1/current.json"

router = APIRouter()


async def fetch_temperature(
    db: AsyncSession, city: City, client: httpx.AsyncClient
) -> None:
    try:
        response = await client.get(
            WEATHER_API_URL,
            params={"key": settings.WEATHER_API_KEY, "q": city.name}
        )
        data = response.json()
        temperature_data = schemas.TemperatureCreate(
            city_id=city.id,
            date_time=datetime.now(),
            temperature=data["current"]["temp_c"],
        )
        await crud.post_temperature(db, temperature_data)
    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/temperatures/update/", response_model=dict)
async def update_temperatures(db: AsyncSession = Depends(get_db)):
    cities = await get_city_list(db=db)
    if not cities:
        raise HTTPException(status_code=404, detail="No cities found")

    async with httpx.AsyncClient() as client:
        tasks: list = []
        for city in cities:

            async def process_city(city: City):
                async for individual_db in get_db():
                    await fetch_temperature(
                        db=individual_db, city=city, client=client
                    )

            tasks.append(process_city(city=city))
        await asyncio.gather(*tasks)
    return {"message": "Temperatures updated successfully"}


@router.get("/temperatures/", response_model=list[schemas.Temperature])
async def detail_temperature(city_id: int = None, db: AsyncSession = Depends(get_db)):
    if city_id:
        return await crud.get_temperature_by_city_id(city_id=city_id, db=db)
    return await crud.get_temperature_list(db=db)
