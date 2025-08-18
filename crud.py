from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from models import City, Temperature
from schemas import CityCreate, CityUpdate


def get_cities(db: Session):
    result = db.execute(select(City))
    cities = result.scalars().all()
    if not cities:
        raise HTTPException(status_code=404, detail="Cities not found")
    return cities

def get_city_by_id(city_id: int, db: Session):
    result = db.execute(select(City).where(City.id == city_id))
    city = result.scalar_one_or_none()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city

def create_city(city: CityCreate, db: Session):
    new_city = City(
        name = city.name,
        additional_info=city.additional_info,
    )
    db.add(new_city)
    db.commit()
    db.refresh(new_city)
    return new_city

def update_city(city_id: int, city: CityUpdate, db: Session):
    result= db.execute(select(City).where(City.id == city_id))
    old_city = result.scalar_one_or_none()
    if not old_city:
        raise HTTPException(status_code=404, detail="City not found")

    old_city.name = city.name
    old_city.additional_info = city.additional_info

    db.commit()
    db.refresh(old_city)
    return old_city

def delete_city(city_id: int, db: Session):
    result = db.execute(select(City).where(City.id == city_id))
    city = result.scalar_one_or_none()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    db.delete(city)
    db.commit()
    return {"detail": f"City with id {city_id} deleted successfully"}


def get_temperatures(db: Session):
    result = db.execute(select(Temperature))
    temperatures = result.scalars().all()
    return temperatures

def get_temperatures_by_city_id(city_id: int, db: Session):
    result = db.execute(
        select(Temperature).where(Temperature.city_id == city_id)
    )
    return result.scalars().all()


import httpx
from datetime import datetime

OPEN_METEO_GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
OPEN_METEO_WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

async def fetch_city_temperature(city_name: str) -> float:
    async with httpx.AsyncClient() as client:
        geo_response = await client.get(OPEN_METEO_GEOCODING_URL, params={"name": city_name, "count": 1})
        geo_data = geo_response.json()

        if not geo_data.get("results"):
            raise ValueError(f"City '{city_name}' not found in geocoding API")

        lat = geo_data["results"][0]["latitude"]
        lon = geo_data["results"][0]["longitude"]

        weather_response = await client.get(OPEN_METEO_WEATHER_URL, params={
            "latitude": lat,
            "longitude": lon,
            "current_weather": True
        })
        weather_data = weather_response.json()

        return weather_data["current_weather"]["temperature"]

