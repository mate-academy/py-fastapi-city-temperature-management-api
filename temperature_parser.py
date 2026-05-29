import os

import httpx
from sqlalchemy import select
from sqlalchemy.orm import Session

import models

import datetime

from dotenv import load_dotenv


load_dotenv()


async def get_temperature_data(cities, db: Session):
    api_key = os.getenv("API_KEY")

    async with httpx.AsyncClient() as client:
        for city in cities:
            temperature_data = await client.get(f"https://weatherapi.com/v1/current.json?key={api_key}&q={city.name}&aqi=no")

            if temperature_data.status_code == 200:
                data = temperature_data.json()
                temperature = data["current"]["temp_c"]

                temperature = models.Temperature(
                    city_id=city.id,
                    date_time=datetime.date.today(),
                    temperature=temperature
                )
                db.add(temperature)
                db.commit()
                db.refresh(temperature)
            else:
                continue

    return db.scalars(select(models.Temperature)).all()
