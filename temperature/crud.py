import httpx
import asyncio
from datetime import datetime
from sqlalchemy.orm import Session
from city import crud as city_crud
from temperature import models


async def fetch_temperature_for_city(city_name: str) -> float | None:
  try:
    async with httpx.AsyncClient() as client:
      geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1"
      geo_response = await client.get(geo_url)
      geo_data = geo_response.json()

      if not geo_data.get("results"):
        return None

      lat = geo_data["results"][0]["latitude"]
      lon = geo_data["results"][0]["longitude"]

      weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m"
      weather_response = await client.get(weather_url)
      weather_data = weather_response.json()

      return weather_data["current"]["temperature_2m"]
  except Exception:
    return None


async def update_temperatures_for_all_cities(db: Session):
  cities = city_crud.get_cities(
      db, limit=1000
  )


  tasks = [fetch_temperature_for_city(city.name) for city in cities]
  temperatures = await asyncio.gather(*tasks)

  records_created = 0
  for city, temp in zip(cities, temperatures):
    if temp is not None:
      db_temp = models.Temperature(
          temperature=temp, date_time=datetime.utcnow(), city_id=city.id
      )
      db.add(db_temp)
      records_created += 1

  db.commit()
  return records_created


def get_all_temperatures(db: Session):
    return db.query(models.Temperature).all()


def get_temperature_by_city_id(db: Session, city_id: int):
    return (
        db.query(models.Temperature)
        .filter(models.Temperature.city_id == city_id)
        .all()
    )