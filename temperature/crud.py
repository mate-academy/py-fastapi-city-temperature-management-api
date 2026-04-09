import os

import httpx
from dotenv import load_dotenv
from sqlalchemy.orm import Session

from temperature import models


load_dotenv()

API_KEY = os.getenv("API_KEY")
URL = "https://api.weatherapi.com/v1/current.json"


async def fetch_temperature(city_name: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            URL,
            params={
                "key": API_KEY,
                "q": city_name
            }
        )
        response.raise_for_status()
        return response.json()


def get_temperature_list(db: Session):
    return db.query(models.Temperature).all()


def get_city_temperature(db: Session, city_id: int):
    return (
        db.query(models.Temperature).filter(models.Temperature.city_id == city_id).all()
    )
