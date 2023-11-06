import os

from datetime import datetime
from dotenv import load_dotenv

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from httpx import AsyncClient

from city import crud as city_crud
from dependencies import get_db
from temperature import crud
from temperature.schemas import Temperature, TemperatureCreate

router = APIRouter()

load_dotenv()

URL = "https://api.weatherapi.com/v1/current.json"
API_KEY = os.environ["API_KEY"]


@router.get("/temperatures/", response_model=list[Temperature])
def read_temperature(db: Session = Depends(get_db), city_id: int | None = None):
    return crud.get_all_temperatures(
        db=db, city_id=city_id
    )


@router.put("/temperatures/update/")
async def update_temperatures(db: Session = Depends(get_db)):
    cities = get_cities_from_database(db)
    for city in cities:
        params = {
            "key": API_KEY,
            "q": city.name
        }
        async with AsyncClient() as client:
            try:
                response = await client.get(URL, params=params)
                if response.status_code == 200:
                    temperature_data = response.json()
                    date_time = datetime.now()
                    temperature = temperature_data["current"]["temp_c"]
                    temperature_create = TemperatureCreate(
                        city_id=city.id,
                        date_time=date_time,
                        temperature=temperature
                    )
                    crud.create_temperature(db, temperature_create)
                else:
                    raise HTTPException(
                        status_code=response.status_code,
                        detail="Failed to fetch temperature data"
                    )

            except Exception as e:
                print(f"Failed to fetch temperature for city {city.name}: {str(e)}")


def get_cities_from_database(db: Session = Depends(get_db)):
    return city_crud.get_all_city(db=db)

