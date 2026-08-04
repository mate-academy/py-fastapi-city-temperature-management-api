import httpx
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
import crud
import schemas
from database import get_db

router = APIRouter(
    prefix="/temperatures",
    tags=["Temperatures"]
)


@router.post("/update", status_code=status.HTTP_200_OK)
async def update_temperatures(db: Session = Depends(get_db)):
    cities = crud.get_cities(db)
    if not cities:
        raise HTTPException(status_code=400, detail="No cities in database to update")

    results = []

    async with httpx.AsyncClient() as client:
        for city in cities:
            try:
                geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city.name}&count=1"
                geo_response = await client.get(geo_url)
                geo_data = geo_response.json()

                if not geo_data.get("results"):
                    results.append({"city": city.name, "status": "error", "detail": "Coordinates not found"})
                    continue

                lat = geo_data["results"][0]["latitude"]
                lon = geo_data["results"][0]["longitude"]

                weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
                weather_response = await client.get(weather_url)
                weather_data = weather_response.json()

                temp_celsius = weather_data["current_weather"]["temperature"]

                crud.create_temperature(db=db, city_id=city.id, temp_val=temp_celsius)
                results.append({"city": city.name, "status": "success", "temperature": temp_celsius})

            except Exception as e:
                results.append({"city": city.name, "status": "error", "detail": str(e)})

    return {"message": "Update complete", "details": results}


@router.get("/", response_model=list[schemas.Temperature])
def read_temperatures(city_id: Optional[int] = None, db: Session = Depends(get_db)):
    return crud.get_temperatures(db, city_id=city_id)
