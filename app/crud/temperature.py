from sqlalchemy.orm import Session
from app.models.temperature import Temperature
from app.models.city import City
import requests

from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("OPENWEATHER_API_KEY")


def fetch_and_store_temperatures(db: Session):
    cities = db.query(City).all()
    for city in cities:
        response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city.name}&appid={api_key}")
        data = response.json()
        temperature = data["main"]["temp"]

        db_temperature = Temperature(
            city_id=city.id,
            temperature=temperature
        )
        db.add(db_temperature)
        db.commit()
        db.refresh(db_temperature)
    return "Temperatures updated"


def get_temperatures(db: Session):
    return db.query(Temperature).all()


def get_temperatures_by_city(db: Session, city_id: int):
    return db.query(Temperature).filter(Temperature.city_id == city_id).all()
