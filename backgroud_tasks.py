import datetime
import os
from sqlalchemy.orm import Session
from fastapi import BackgroundTasks

import httpx
from dotenv import load_dotenv

from temperature import models as temperature_models
from temperature import crud as temperature_crud
from cities import models as cities_models


load_dotenv()

API_KEY = os.getenv("API_KEY")
URL = "http://api.weatherapi.com/v1/current.json"


async def get_weather_data(city_name: str) -> float | None:
    async with httpx.AsyncClient() as client:
        filtering = city_name
        print(f"Performing request to Weather API for city {filtering}...")
        result = await client.get(URL, params={"key": API_KEY, "q": filtering})
        if result.status_code >= 400:
            print(f"Request failed with status code {result.status_code}\n"
                  f"{result.text}")
            return

        result = result.json()
        temp_c = result["current"]["temp_c"]
        return temp_c


async def update_weather_data(
        city: cities_models.City,
        temperature_id: int,
        db: Session,
        background_tasks: BackgroundTasks
) -> None:
    temp = await get_weather_data(city.name)
    db_temperature = db.query(temperature_models.Temperature).filter(
        temperature_models.Temperature.id == temperature_id
    ).first()

    if not db_temperature:
        await temperature_crud.create_city_temperature(
            db=db,
            city=city,
            background_tasks=background_tasks
        )
        return

    db_temperature.temperature = temp
    db_temperature.date_time = datetime.datetime.now()
    db.commit()
    db.refresh(db_temperature)
