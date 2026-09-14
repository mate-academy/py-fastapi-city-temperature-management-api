import httpx
import asyncio

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal

from Temperature import schemas
from Temperature import crud


router = APIRouter()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.post(
    "/temperatures/update/",
    response_model=list[schemas.TemperatureAdded]
)
async def update_temperature(
        db: Session = Depends(get_db)
):
    cities = crud.get_all_city(db=db)
    updated_temperatures = []

    async with httpx.AsyncClient() as client:
        for city in cities:
            await asyncio.gather()

            url_parameters_city = (
                f"https://geocoding-api.open-meteo.com/v1/search"
                f"?name={city.name}"
            )
            response = await client.get(url_parameters_city)
            geo = response.json()

            if not geo.get("results"):
                continue

            lat = geo["results"][0]["latitude"]
            lon = geo["results"][0]["longitude"]

            params = {
                "latitude": lat,
                "longitude": lon,
                "current": "temperature_2m",
            }

            weather_response = await client.get(
                "https://api.open-meteo.com/v1/forecast/",
                params=params
            )
            weather_json = weather_response.json()

            current_temperature = weather_json["current"]["temperature_2m"]
            current_time = weather_json["current"]["time"]

            temperature_date = schemas.TemperatureAdded(
                city_id=city.id,
                date_time=current_time,
                temperature=current_temperature,
            )

            save_temperature = crud.update_temperature_city(
                db=db,
                temperature=temperature_date
            )
            updated_temperatures.append(save_temperature)

        return updated_temperatures


@router.get("/temperatures/", response_model=list[schemas.Temperature])
def get_temperature_id(
        city_id: int = None,
        db: Session = Depends(get_db)
):

    if city_id is not None:
        return crud.get_temperature_by_city_id(db=db, city_id=city_id)
    return crud.get_all_temperature(db=db)
