import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependencies import get_db
import city.crud as city_crud
from temperature import schemas, crud, models
import httpx
from settings import OPEN_WEATHER_MAP_KEY

router = APIRouter()
URL = "https://api.openweathermap.org/data/2.5/weather"


@router.get("/temperatures/", response_model=list[schemas.Temperature])
def get_temperatures(
    city_id: int | None = None, db: Session = Depends(get_db)
) -> list[models.DBTemperature]:
    return crud.get_all_temperature(db, city_id)


async def fetch_temperature(city_name: str) -> float:
    async with httpx.AsyncClient() as client:
        res = await client.get(
            URL,
            params={
                "q": city_name,
                "appid": OPEN_WEATHER_MAP_KEY,
                "units": "metric",
            },
        )
        res.raise_for_status()

    return res.json()["main"]["temp"]


@router.post("/temperatures/update")
async def update_temperature(
    db: Session = Depends(get_db),
) -> dict[str, list[str]]:
    temperature_for_cities = []
    cities = city_crud.get_all_cities(db)
    updated = []
    failed = []
    for city in cities:
        try:
            temperature = await fetch_temperature(city.name)
            updated.append(city.name)
        except httpx.HTTPStatusError:
            failed.append(city.name)
            continue

        temperature_for_city = {
            "city_id": city.id,
            "date_time": datetime.datetime.now(),
            "temperature": temperature,
        }
        temperature_for_cities.append(temperature_for_city)

    crud.create_temperature_list(db, temperature_for_cities)
    return {"updated": updated, "failed": failed}
