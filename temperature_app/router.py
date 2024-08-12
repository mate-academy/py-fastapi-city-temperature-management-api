import os
from city_app import crud as city_crud
from dependencies import get_db
from temperature_app import crud, schemas
import httpx
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()
weather_api_key = os.getenv("WEATHER_API_KEY")


@router.post("/temperatures/update")
async def get_all_temperatures(db: AsyncSession = Depends(get_db)):
    cities = city_crud.get_all_cities(db)
    weather_url = "http://api.weatherapi.com/v1/current.json"
    async with httpx.AsyncClient() as client:
        for city in cities:
            params = {
                "key": weather_api_key,
                "q": city,
            }
            response = await client.get(weather_url, params=params)
            data = response.json()
            temperature_data = schemas.TemperatureCreate(
                city_id=city.id,
                date_time=data["current"]["last_updated"],
                temperature=data["current"]["temp_c"],
            )
            crud.create_temperature(db=db, temperature=temperature_data)
        return {"message": "Temperatures updated"}


@router.get("/temperatures/update", response_model=list[schemas.Temperature])
def get_temperatures(
        db: Session = Depends(get_db)
) -> list[schemas.Temperature]:
    return crud.get_temperature(db)


@router.get("/temperatures/update/{city_id}")
def update_temperatures(
    city_id: int, db: Session = Depends(get_db)
) -> schemas.Temperature:
    return crud.get_specific_temperature_city_id(db=db, city_id=city_id)
