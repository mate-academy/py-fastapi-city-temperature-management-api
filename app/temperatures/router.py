from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy import select
import httpx
import asyncio
from app.database import get_db
from app.cities.models import City
from app.temperatures.models import Temperature
from app.temperatures.schemas import TemperatureResponse

router = APIRouter(prefix="/temperatures", tags=["Temperatures"])


async def fetch_weather_for_city(
        client: httpx.AsyncClient,
        city_name: str
) -> float | None:
    try:
        geo_url = (
            f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&"
            f"count=1&language=en&format=json"
        )
        geo_response = await client.get(geo_url)
        geo_data = geo_response.json()

        if not geo_data.get("results"):
            return None

        lat = geo_data["results"][0]["latitude"]
        lon = geo_data["results"][0]["longitude"]

        weather_url = (
            f"https://api.open-meteo.com/v1/forecast?latitude={lat}&"
            f"longitude={lon}&current_weather=true"
        )
        weather_response = await client.get(weather_url)
        weather_data = weather_response.json()

        return weather_data["current_weather"]["temperature"]
    except Exception:
        return None


@router.post("/update", status_code=status.HTTP_200_OK)
async def update_temperatures(db: Session = Depends(get_db)):
    cities = db.execute(select(City)).scalars().all()
    if not cities:
        return {"message": "No cities found in database to update."}

    updated_count = 0

    async with httpx.AsyncClient() as client:
        tasks = [fetch_weather_for_city(client, city.name) for city in cities]
        temperatures = await asyncio.gather(*tasks)

        for city, temp in zip(cities, temperatures):
            if temp is not None:
                db_temp = Temperature(city_id=city.id, temperature=temp)
                db.add(db_temp)
                updated_count += 1

        db.commit()

    return {
        "message": f"Successfully updated temperatures "
                   f"for {updated_count} cities."
    }


@router.get("/", response_model=list[TemperatureResponse])
def get_temperatures(
        city_id: int | None = None,
        db: Session = Depends(get_db)
) -> list[TemperatureResponse]:
    query = select(Temperature)

    if city_id is not None:
        query = query.where(Temperature.city_id == city_id)

    query = query.order_by(Temperature.date_time.desc())

    records = db.execute(query).scalars().all()
    return records
