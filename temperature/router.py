import os
from datetime import datetime

import httpx
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from city import crud as city_crud
from temperature import crud, schemas
from database import get_db
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/temperatures", tags=["temperatures"])

API_KEY = os.getenv("WEATHER_API_KEY")


@router.post("/update")
async def update_temperatures(db: Session = Depends(get_db)):
    cities = city_crud.get_cities(db=db)
    results = []

    async with httpx.AsyncClient() as client:
        for city in cities:
            try:
                response = await client.get(
                    f"https://api.openweathermap.org/data/2.5/weather",
                    params={
                        "q": city.name,
                        "appid": API_KEY,
                        "units": "metric"
                    }
                )
                data = response.json()
                temp = data["main"]["temp"]
                record = crud.create_temperature(
                    db=db,
                    city_id=city.id,
                    temperature=temp,
                    date_time=datetime.now()
                )
                results.append(record)
            except Exception as e:
                print(f"Error fetching temperature for {city.name}: {e}")
                
    db.commit()
    return {"updated": len(results)}


@router.get("/", response_model=list[schemas.Temperature])
def get_temperatures(city_id: int = None, db: Session = Depends(get_db)):
    return crud.get_temperatures(db=db, city_id=city_id)
