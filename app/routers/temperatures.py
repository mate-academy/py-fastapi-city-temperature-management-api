from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import httpx

from app.database import get_db
from app.models import City, Temperature
from app.schemas import TemperatureList
import app.crud as crud

router = APIRouter(prefix="/temperatures", tags=["Temperatures"])


@router.post("/update")
async def update_temperatures(db: Session = Depends(get_db)):
    cities = db.query(City).all()

    if not cities:
        raise HTTPException(status_code=400, detail="No cities found")

    async with httpx.AsyncClient() as client:
        for city in cities:
            geo_url = (
                "https://geocoding-api.open-meteo.com/v1/search"
                f"?name={city.name}&count=1"
            )
            geo_response = await client.get(geo_url)
            geo_response.raise_for_status()

            geo_data = geo_response.json()
            if not geo_data.get("results"):
                continue

            latitude = geo_data["results"][0]["latitude"]
            longitude = geo_data["results"][0]["longitude"]

            weather_url = (
                "https://api.open-meteo.com/v1/forecast"
                f"?latitude={latitude}&longitude={longitude}&current_weather=true"
            )
            weather_response = await client.get(weather_url)
            weather_response.raise_for_status()

            temperature = weather_response.json()["current_weather"]["temperature"]
            crud.create_temperature(db, city.id, temperature)

    return {"detail": "Temperatures updated successfully"}


@router.get("/", response_model=list[TemperatureList])
def get_temperatures(
    city_id: int | None = None,
    db: Session = Depends(get_db)
):
    return crud.get_temperatures(db, city_id)
