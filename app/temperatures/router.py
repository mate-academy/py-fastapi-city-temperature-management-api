from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
import httpx
from datetime import datetime
from typing import List, Optional

from app.database import get_db
from app.temperatures import crud, schemas
from app.cities import crud as city_crud

router = APIRouter(prefix="/temperatures", tags=["Temperatures"])

@router.post("/update", status_code=status.HTTP_200_OK)
async def update_temperatures(db: Session = Depends(get_db)):
    cities = city_crud.get_cities(db)
    if not cities:
        raise HTTPException(status_code=400, detail="No cities found in database to update.")

    updated_count = 0

    async with httpx.AsyncClient() as client:
        for city in cities:
            try:
                geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city.name}&count=1&language=en&format=json"
                geo_response = await client.get(geo_url)
                geo_data = geo_response.json()

                if not geo_data.get("results"):
                    continue

                lat = geo_data["results"][0]["latitude"]
                lon = geo_data["results"][0]["longitude"]

                weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
                weather_response = await client.get(weather_url)
                weather_data = weather_response.json()

                current_temp = weather_data["current_weather"]["temperature"]

                temp_data = schemas.TemperatureCreate(
                    city_id=city.id,
                    temperature=current_temp,
                    date_time=datetime.utcnow()
                )
                crud.create_temperature_record(db, temp_data)
                updated_count += 1

            except Exception:
                continue

    return {"message": f"Successfully updated temperatures for {updated_count} cities."}


@router.get("/", response_model=List[schemas.Temperature])
def read_temperatures(
    city_id: Optional[int] = Query(None, description="Filter temperature records by City ID"),
    db: Session = Depends(get_db)
):
    return crud.get_temperatures(db, city_id=city_id)
