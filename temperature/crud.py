from datetime import datetime

from sqlalchemy.orm import Session

from temperature import models

import httpx

import asyncio

from city import crud as city_crud



def get_all_temperatures(
    db: Session,
    city_id: int | None = None,
    skip: int = 0,
    limit: int = 100,
):
    queryset = db.query(models.DBTemperature)
    if city_id is not None:
        queryset = queryset.filter(
            models.DBTemperature.city_id == city_id
        )
    return queryset.offset(skip).limit(limit).all()


def create_temperature(
    db: Session,
    city_id: int,
    date_time: datetime,
    temperature: float,
):
    db_temperature = models.DBTemperature(
        city_id=city_id,
        date_time=date_time,
        temperature=temperature,
    )
    db.add(db_temperature)
    db.commit()
    db.refresh(db_temperature)
    return db_temperature


GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"


async def fetch_temperature(city_name: str) -> float | None:
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            geo_response = await client.get(
                GEOCODING_URL,
                params={"name": city_name, "count": 1},
            )
            geo_data = geo_response.json()
            results = geo_data.get("results")
            if not results:
                return None

            latitude = results[0]["latitude"]
            longitude = results[0]["longitude"]

            weather_response = await client.get(
                FORECAST_URL,
                params={
                    "latitude": latitude,
                    "longitude": longitude,
                    "current": "temperature_2m",
                },
            )
            weather_data = weather_response.json()
            return weather_data["current"]["temperature_2m"]
    except httpx.HTTPError:
        return None




async def update_temperatures(db: Session) -> None:
    cities = city_crud.get_all_cities(db)

    temperatures = await asyncio.gather(
        *[fetch_temperature(city.name) for city in cities]
    )

    for city, temperature in zip(cities, temperatures):
        if temperature is not None:
            create_temperature(
                db=db,
                city_id=city.id,
                date_time=datetime.now(),
                temperature=temperature,
            )
