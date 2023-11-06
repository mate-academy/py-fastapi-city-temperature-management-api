import os

import requests
from sqlalchemy.orm import Session

from db.models import DBTemperature, DBCity


API_KEY = os.environ.get(API_KEY)
BASE_URL = "http://api.weatherapi.com/v1/current.json"


def get_all_temperatures(db: Session):
    return db.query(DBTemperature).all()


def get_temperatures_by_city(db: Session, city_id: int):
    temperatures = (
        db.query(DBTemperature).filter(DBTemperature.city_id == city_id).all()
    )
    return temperatures


def fetch_temperature_data(db: Session) -> None:
    cities = db.query(DBCity).all()
    for city in cities:
        city_name = city.name
        request_url = f"{BASE_URL}?key={API_KEY}&q={city_name}"
        response = requests.get(request_url)
        try:
            if response.status_code == 200:
                data = response.json()
                temperature = data.get("current", {}).get("temp_c")
                if temperature:
                    db_temperature = DBTemperature(
                        city_id=city.id, temperature=temperature
                    )
                    db.add(db_temperature)
        except Exception as e:
            print(f"Failed to fetch data for city {city_name}: {str(e)}")

    db.commit()
