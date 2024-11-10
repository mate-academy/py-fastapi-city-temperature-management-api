import httpx
from sqlalchemy.orm import Session
from datetime import datetime
from application import models, schemas


async def fetch_temperature(city_name: str, api_key: str) -> float | None:
    url = "http://api.openweathermap.org/data/2.5/weather"
    params = {"q": city_name, "appid": api_key}

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            if "main" in data and "temp" in data["main"]:
                temperature = data["main"]["temp"] - 273.15
                return temperature
    except (httpx.RequestError, httpx.HTTPStatusError, KeyError) as e:
        print(f"Error fetching temperature: {e}")

    return None

async def update_temperatures(db: Session):
    cities = db.query(models.City).all()
    for city in cities:
        temperature = await fetch_temperature(city.name)
        if temperature is not None:
            temperature_record = models.Temperature(
                city_id=city.id,
                date_time=datetime.now(),
                temperature=temperature
            )
            db.add(temperature_record)
    db.commit()
