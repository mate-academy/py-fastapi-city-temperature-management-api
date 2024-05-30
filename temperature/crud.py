import asyncio
import datetime

import httpx
import pytz
from sqlalchemy.orm import Session

from city import crud as city_crud
from temperature import schemas, models
from settings import settings


API_KEY = settings.weather_api_key
WEATHER_API_URL = settings.weather_api_url
TIME_ZONE = pytz.timezone(settings.time_zone)


def create_temperature(
    db: Session,
    temp_schema: schemas.TemperatureBase
) -> schemas.Temperature:

    db_temperature = models.Temperature(**temp_schema.model_dump())
    db.add(db_temperature)
    db.commit()
    db.refresh(db_temperature)

    return db_temperature


def get_temperatures(db: Session, city_id: int | None = None) -> list[schemas.Temperature]:
    query = db.query(models.Temperature)
    if city_id:
        query = query.filter(models.Temperature.city_id == city_id)

    return query.all()


async def get_city_temp(url: str, params: dict, client) -> int:
    resp = await client.get(url=url, params=params)
    data = resp.json()

    return data["current"]["temp_c"]


async def set_temps(db: Session) -> None:
    db_cities = city_crud.get_all_cities(db=db)
    city_names = [city.name for city in db_cities]

    async with httpx.AsyncClient() as client:
        tasks = []

        for city in city_names:
            params = {"key": API_KEY, "q": city}
            tasks.append(
                asyncio.ensure_future(
                    get_city_temp(
                        url=WEATHER_API_URL,
                        params=params,
                        client=client
                    )
                )
            )

        temperatures = await asyncio.gather(*tasks)
        for i in range(len(db_cities)):
            temp_schema = schemas.TemperatureBase(
                city_id=db_cities[i].id,
                date_time=datetime.datetime.now(tz=TIME_ZONE),
                temperature=int(temperatures[i])
            )
            create_temperature(db=db, temp_schema=temp_schema)
