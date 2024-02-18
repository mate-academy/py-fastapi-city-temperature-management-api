import aiohttp
import os
from dependencies import db_dependency
from temperatures import models
from cities import crud as crud_city
import temperatures.schemas as temp_schemas
from fastapi import HTTPException
from dotenv import load_dotenv

load_dotenv()


def get_all_temperatures(
    db: db_dependency, city_id: int | None = None
) -> list[models.Temperature] | models.Temperature:
    queryset = db.query(models.Temperature)

    if city_id is not None:
        return queryset.filter(models.Temperature.city_id == city_id).first()

    return queryset.all()


def create_temperature(
    db: db_dependency,
    temperature: temp_schemas.TemperatureCreate,
) -> None:
    db_temperature = (
        db.query(models.Temperature)
        .filter(models.Temperature.city_id == temperature.city_id)
        .first()
    )

    if db_temperature is None:
        db_temperature = models.Temperature(
            temperature=temperature.temperature, city_id=temperature.city_id
        )
    else:
        db_temperature.temperature = temperature.temperature

    db.add(db_temperature)
    db.commit()
    db.refresh(db_temperature)


async def update_temperature(
    db: db_dependency,
) -> None:
    try:
        API_KEY = os.getenv("API_KEY")

        cities = crud_city.get_all_cities(db)

        for city in cities:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city.name}&appid={API_KEY}&units=metric"
            response = await fetch_temperature(url)

            temperature = response.get("main", {}).get("temp")
            temperature_data = temp_schemas.TemperatureCreate(
                city_id=city.id, temperature=temperature
            )
            create_temperature(db=db, temperature=temperature_data)

    except Exception as e:
        print(f"Error fetching temperature data: {e}.")
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch temperature data. Please check correct name of cities.",
        )


async def fetch_temperature(url: str) -> None:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response.raise_for_status()
            return await response.json()
