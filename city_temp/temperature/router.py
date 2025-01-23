import os
from dotenv import load_dotenv
import httpx
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from city_temp.city.models import City as CityModel
from city_temp.temperature.crud import (
    create_temperature,
    get_temperatures,
    get_temperatures_by_city,
)
from city_temp.temperature.schemas import Temperature
from database import SessionLocal


load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter()


@router.get("/temperatures/", response_model=list[Temperature])
def get_all_temperatures(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return get_temperatures(db=db, skip=skip, limit=limit)


async def fetch_temperature_for_city(city):
    print(f"Fetching temperature for city: {city.name}")

    async with httpx.AsyncClient() as client:
        url = (
            f"https://api.openweathermap.org/data/2.5/weather?q={city.name}"
            f"&appid={API_KEY}&units=metric/"
        )
        response = await client.get(url)

        if response.status_code == 200:
            data = response.json()
            temperature = data["main"]["temp"]
            print(f"Fetched temperature for {city.name}: {temperature}")
            return temperature

        else:
            print(
                f"Failed to fetch temperature for {city.name}. "
                f"Status: {response.status_code}"
            )
            return None


@router.post("/temperatures/update/", response_model=list[Temperature])
async def update_temperatures(db: Session = Depends(get_db)):
    cities = db.query(CityModel).all()
    updated_records = []

    for city in cities:
        temperature = await fetch_temperature_for_city(city)

        if temperature:
            db_temperature = create_temperature(db, city, temperature)
            updated_records.append(Temperature.from_orm(db_temperature))

        else:
            print(f"Skipping update for the city: {city.name}")
        print("\n")

    return updated_records


@router.get("/temperatures/by_city/")
def get_temperature_by_city(city_id: int, db: Session = Depends(get_db)):
    temperatures = get_temperatures_by_city(db=db, city_id=city_id)

    if not temperatures:
        raise HTTPException(
            status_code=404,
            detail="Temperature records not found for this city",
        )

    return temperatures
