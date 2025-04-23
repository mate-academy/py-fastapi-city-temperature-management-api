from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from temperature import schemas, crud
from city import models
from datetime import datetime
import os
import httpx
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

router = APIRouter(
    prefix="/temperatures",
    tags=["Temperatures"]
)

@router.get("/", response_model=list[schemas.Temperature])
def read_all_temperatures(db: Session = Depends(get_db)):
    return crud.get_all_temperatures(db)

@router.get("/by_city/", response_model=list[schemas.Temperature])
def read_temperatures_by_city(city_id: int, db: Session = Depends(get_db)):
    return crud.get_temperatures_by_city(db, city_id)

@router.post("/update")
async def update_temperatures(db: Session = Depends(get_db)):
    cities = db.query(models.City).all()
    if not cities:
        raise HTTPException(status_code=404, detail="No cities in database")

    async with httpx.AsyncClient() as client:
        for city in cities:
            response = await client.get(
                "https://api.openweathermap.org/data/2.5/weather",
                params={
                    "q": city.name,
                    "appid": API_KEY,
                    "units": "metric",
                    "lang": "en"
                }
            )
            if response.status_code != 200:
                continue

            data = response.json()
            temp_celsius = data["main"]["temp"]

            temp = schemas.TemperatureCreate(
                city_id=city.id,
                date_time=datetime.utcnow(),
                temperature=temp_celsius
            )
            crud.create_temperature(db, temp)

    return {"message": "Temperature data updated from OpenWeatherMap"}
