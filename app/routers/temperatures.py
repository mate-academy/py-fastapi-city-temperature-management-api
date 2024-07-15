import logging
from datetime import datetime
from typing import List
import os

import aiohttp
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dotenv import load_dotenv


from app import crud, schemas
from app.dependencies import get_db


load_dotenv()

API_KEY = os.getenv("API_KEY")

router = APIRouter()


@router.post("/update", response_model=List[schemas.Temperature])
async def update_temperatures(
        db: Session = Depends(get_db)
) -> List[schemas.Temperature]:
    cities = crud.get_cities(db)
    temperatures = []
    async with aiohttp.ClientSession() as session:
        for city in cities:
            url = "https://api.openweathermap.org/data/2.5/weather"
            params = {
                "q": city.name,
                "appid": API_KEY
            }
            async with session.get(url, params=params) as response:
                if response.status != 200:
                    logging.error(
                        f"Failed to fetch weather data for city: {city.name},"
                        f" status: {response.status}"
                    )
                    continue
                data = await response.json()
                logging.info(f"Received data for city {city.name}: {data}")

                if "main" not in data:
                    logging.error(
                        f"No 'main' key in response data for city: {city.name}"
                    )
                    continue

                temperature = data["main"]["temp"] - 273.15
                temp_record = schemas.TemperatureCreate(
                    city_id=city.id,
                    date_time=datetime.now(),
                    temperature=temperature,
                )
                created_temp = crud.create_temperature(
                    db=db, temperature=temp_record
                )
                temperatures.append(created_temp)

    return temperatures


@router.get("/", response_model=List[schemas.Temperature])
def read_temperatures(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> List[schemas.Temperature]:
    temperatures = crud.get_temperatures(db, skip=skip, limit=limit)
    return temperatures


@router.get("/by_city", response_model=List[schemas.Temperature])
def read_temperatures_by_city(
    city_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
) -> List[schemas.Temperature]:
    temperatures = crud.get_temperatures_by_city(
        db, city_id=city_id, skip=skip, limit=limit
    )
    return temperatures
