import asyncio

import requests
from sqlalchemy.orm import Session

from city.models import DBCity
from settings import settings
from temperature.models import DBTemperature
from temperature.schemas import OnlineResponse


async def get_temperature_for_city(city_name: str, city_id: int, api_key: str):
    try:
        response = requests.get(
            f"{settings.OPEN_WEATHER_API_URL}q={city_name}&appid={api_key}"
            )
        data = response.json()
        temperature = data['main']['temp']
        current_date = data['dt']
        db_temperature = DBTemperature(
            city_id=city_id,
            date_time=current_date,
            temperature=round(temperature - settings.KELVIN_TO_CELSIUS, 1)
        )
        return db_temperature
    except (requests.RequestException, KeyError) as e:
        print(f"Error fetching data for city {city_id}: {e}")
        return

async def update_temperature_for_cities(db: Session) -> dict:
    cities = db.query(DBCity).all()
    coroutines = [get_temperature_for_city(city.name, city.id, settings.OPEN_WEATHER_API_KEY) for city in cities]
    db_temperature_objects: list[DBTemperature] = await asyncio.gather(*coroutines)
    db_temperature_objects = [db_temperature for db_temperature in db_temperature_objects if db_temperature is not None]
    for db_temperature_object in db_temperature_objects:
        db.add(db_temperature_object)
        db.commit()
        db.refresh(db_temperature_object)
    if len(cities) != len(db_temperature_objects):
        return OnlineResponse(status="error", message="Temperatures updated, but some cities could not be updated")
    else:
        return OnlineResponse(status="success", message="All temperatures updated")

def get_list_of_all_temperature_records(
        db: Session,
        skip: int,
        limit: int
):
    return db.query(DBTemperature).offset(skip).limit(limit).all()

def get_temperature_by_city_id(db: Session, city_id: int):
    return db.query(DBTemperature).filter(DBTemperature.city_id == city_id).all()