import os
from typing import Optional, List
import httpx
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas, database, models
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("WEATHER_API_KEY")
router = APIRouter()

@router.get("/temperatures/", response_model=List[schemas.Temperature])
def get_temperatures(
        city_id: Optional[int] = None, db: Session = Depends(database.get_db)
):

    if city_id:
        city = crud.get_city(db, city_id=city_id)
        if not city:
            raise HTTPException(status_code=404, detail="City not found")
        temperatures = db.query(
            models.Temperature).filter(
            models.Temperature.city_id == city_id).all()
    else:
        temperatures = db.query(models.Temperature).all()

    return temperatures

@router.post("/temperatures/update")
async def update_temperatures(db: Session = Depends(database.get_db)):

    cities = crud.get_cities(db)
    if not cities:
        raise HTTPException(
            status_code=404, detail="No cities found in the database."
        )

    async with httpx.AsyncClient() as client:
        for city in cities:
            try:

                response = await client.get(
                    f"https://api.openweathermap.org/data/2.5/weather?q="
                    f"{city.name}&appid={api_key}")
                response.raise_for_status()
                temp_data = response.json()

                temperature_kelvin = temp_data["main"]["temp"]
                temperature_celsius = temperature_kelvin - 273.15


                new_temp = models.Temperature(
                    city_id=city.id,
                    date_time=datetime.now(),
                    temperature=temperature_celsius
                )
                db.add(new_temp)
            except httpx.HTTPStatusError as e:
                print(f"Failed to fetch temperature for {city.name}: {e}")
            except KeyError:
                print(f"Unexpected response format{city.name}: {temp_data}")

    db.commit()
    return {"message": "Temperatures updated successfully"}
