import httpx
from sqlalchemy.orm import Session
from datetime import datetime
from app import models, schemas


async def fetch_temperature(city_name: str):
    response = await httpx.get(f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid=YOUR_API_KEY")
    if response.status_code == 200:
        data = response.json()
        temperature = data["main"]["temp"] - 273.15
        return temperature
    return None

async def update_temperatures(db: Session):
    cities = db.query(models.City).all()
    for city in cities:
        temperature = await fetch_temperature(city.name)
        if temperature is not None:
            temperature_record = models.Temperature(
                city_id=city.id,
                date_time=datetime.now(),
                temperature=temperature
            )
            db.add(temperature_record)
    db.commit()
