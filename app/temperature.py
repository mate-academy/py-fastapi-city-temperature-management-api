from sqlalchemy.orm import Session
from app.models import Temperature, City
from datetime import datetime


async def fetch_temperature(city_name: str) -> float:
    return 20.0


async def update_temperatures(db: Session):
    cities = db.query(City).all()
    for city in cities:
        temperature = await fetch_temperature(city.name)
        temp_record = Temperature(
            city_id=city.id,
            date_time=datetime.now(),
            temperature=temperature
        )
        db.add(temp_record)
    db.commit()
