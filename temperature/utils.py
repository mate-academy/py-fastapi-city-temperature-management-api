import os

import requests
from sqlalchemy.orm import Session
from fastapi import HTTPException

from city import crud as city_crud
from temperature import crud as temperature_crud
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
URL = "http://api.weatherapi.com/v1/current.json"


def fetch_temperature_data(db: Session, city_name: str):
    params = {
        "key": API_KEY,
        "q": city_name
    }
    response = requests.get(URL, params=params)

    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to fetch temperature data")

    response = response.json()
    current_weather = response["current"]
    temp_c = current_weather["temp_c"]
    return temp_c


def update_temperatures(db: Session):
    cities = city_crud.get_all_cities(db=db)
    for city in cities:
        temperature = fetch_temperature_data(db=db, city_name=city.name)
        temperature_crud.update_temperatures_from_api(db=db, city_id=city.id, temperature=temperature)

    return {"message": "Temperature data updated for all cities"}
