import os
import httpx

from dotenv import load_dotenv
from sqlalchemy.orm import Session
from temperature.models import DBTemperature

load_dotenv()

API_KEY = os.environ.get("API_KEY")
BASE_URL = "http://api.weatherapi.com/v1/current.json"


def get_temperatures(db: Session):
    return db.query(DBTemperature).all()


def get_temperatures_by_city(db: Session, city_id: int):
    return (
        db.query(DBTemperature).filter(DBTemperature.city_id == city_id).all()
    )


async def fetch_temperature(city_name):
    try:
        async with httpx.AsyncClient() as client:
            url = f"{BASE_URL}?key={API_KEY}&q={city_name}"
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            temperature = data["current"]["temp_c"]
            return temperature
    except Exception as e:
        print(f"Error in finding city {city_name}: {e}")
        return None


async def update_temperatures(db: Session):
    from city.models import DBCity
    from temperature.models import DBTemperature

    cities = db.query(DBCity).all()

    for city in cities:
        temperature = await fetch_temperature(city.name)
        if temperature:
            db_temperature = DBTemperature(
                city_id=city.id, temperature=temperature
            )
            db.add(db_temperature)
            db.commit()


async def temperature_update_starter():
    from database import engine
    from sqlalchemy.orm import sessionmaker

    SessionLocal = sessionmaker(bind=engine)

    async with SessionLocal() as db:
        await update_temperatures(db)
