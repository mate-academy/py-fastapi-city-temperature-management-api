import os
import aiohttp
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import Temperature, City

router = APIRouter()

async def fetch_temperature(city_name: str):
    async with aiohttp.ClientSession() as session:
        API_KEY = os.getenv("WEATHER_API_KEY")
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric"
        async with session.get(url) as response:
            data = await response.json()
            return data["main"]["temp"]

@router.post("/temperatures/update")
async def update_temperatures(db: Session = Depends(SessionLocal)):
    cities = db.query(City).all()
    for city in cities:
        temp = await fetch_temperature(city.name)
        temperature = Temperature(city_id=city.id, temperature=temp)
        db.add(temperature)
    db.commit()
    return {"message": "Temperatures updated"}

@router.get("/temperatures")
def read_temperatures(db: Session = Depends(get_db)):
    temperatures = db.query(Temperature).all()
    return temperatures


@router.get("/temperatures")
def read_city_temperatures(city_id: int, db: Session = Depends(get_db)):
    temperatures = db.query(Temperature).filter(Temperature.city_id == city_id).all()
    return temperatures