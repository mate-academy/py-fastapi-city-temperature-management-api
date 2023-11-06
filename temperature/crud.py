import os
from datetime import datetime

import requests
import httpx
from dotenv import load_dotenv
from fastapi import HTTPException
from sqlalchemy.orm import Session


from . import models
from city.crud import get_all_cities


load_dotenv()


URL = "http://api.weatherapi.com/v1/current.json"


def get_all_temperatures(db: Session):
    return db.query(models.Temperature).all()


def get_temperature_by_city_id(db: Session, city_id: int):
    db_temperature = db.query(models.Temperature).filter(
        models.Temperature.city_id == city_id
    ).first()

    if db_temperature is None:
        raise HTTPException(status_code=404, detail="City not found")

    return db_temperature


def get_weather_data(url: str, params: dict):

    print(f"fetching temperature for {params['q']}")

    weather = requests.get(url=url, params=params).json()
    current_weather = weather["current"]

    date_time = current_weather["last_updated"]
    temperature = current_weather["temp_c"]

    print(f"stopped fetching temperature for {params['q']}")

    return date_time, temperature


def change_temperature_status(
        db: Session,
        city_id: int,
        date_time: str,
        temperature: int
):
    try:
        weather = get_temperature_by_city_id(db=db, city_id=city_id)
    except HTTPException:
        db_weather = models.Temperature(
            city_id=city_id,
            date_time=datetime.strptime(date_time, "%Y-%m-%d %H:%M"),
            temperature=temperature
        )
        db.add(db_weather)
        db.commit()
        db.refresh(db_weather)
    else:
        weather.date_time = datetime.strptime(date_time, "%Y-%m-%d %H:%M")
        weather.temperature = temperature
        db.commit()


def update_temperatures(db: Session):
    cities = get_all_cities(db)

    params = {
        "q": "Paris",
        "key": os.environ.get("WEATHER_API_KEY")
    }

    for city in cities:
        params["q"] = city.name
        city_id = city.id
        date_time, temperature = get_weather_data(url=URL, params=params)
        change_temperature_status(
            db=db,
            city_id=city_id,
            date_time=date_time,
            temperature=temperature
        )
