import datetime
from typing import List
import httpx

from sqlalchemy.orm import Session

from temperature import models, schemas
from city.crud import get_all_cities
from settings import settings

API_KEY = settings.WEATHER_API_KEY
WEATHER_API_URL = settings.WEATHER_API_URL


def get_temperatures(
        db: Session,
        city_id: int | None = None
) -> list[schemas.Temperature]:
    query = db.query(models.Temperature)
    if city_id:
        query = query.filter(models.Temperature.city_id == city_id)

    return query.all()


async def fetch_temperature(city_name: str) -> dict[str, str] | None:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            url=WEATHER_API_URL,
            params={"key": API_KEY, "q": city_name}
        )
        data = response.json()
        data_current = data.get("current")
        if data_current:
            last_updated = data_current.get("last_updated")
            temperature = data_current.get("temp_c")
            return {"date_time": last_updated, "temperature": temperature}
        return None


async def fetch_temperatures_for_cities(db: Session) -> List[models.Temperature]:
    cities = get_all_cities(db=db)
    temperatures = []
    for city in cities:
        temperature = await fetch_temperature(city_name=city.name)
        if temperature is not None:
            temperatures.append(models.Temperature(
                city_id=city.id,
                date_time=temperature.get("date_time"),
                temperature=temperature.get("temperature")))
    return temperatures


async def update_temperatures(db: Session) -> None:
    temperatures = await fetch_temperatures_for_cities(db)
    for temp in temperatures:
        if temp.date_time is not None:
            temp.date_time = datetime.datetime.strptime(temp.date_time, '%Y-%m-%d %H:%M')
            db.add(temp)
    db.commit()
