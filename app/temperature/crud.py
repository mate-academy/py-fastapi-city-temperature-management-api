import asyncio

from sqlalchemy.orm import Session

from app.temperature.models import Temperature
from app.city.models import City
from app.weather_service import fetch_temperature


async def update_temperature(db: Session):
    cities = db.query(City).all()
    tasks = [fetch_temperature(city) for city in cities]
    results = await asyncio.gather(*tasks)

    temperatures = [
        Temperature(
            city_id=result["city_id"],
            date_time=result["date_time"],
            temperature=result["temperature"],
        )
        for result in results
    ]

    db.bulk_save_objects(temperatures)
    db.commit()

    return temperatures


def get_temperatures(db: Session):
    return db.query(Temperature).all()


def get_temperature_by_city_id(db: Session, city_id: int):
    return db.query(Temperature).filter(
        Temperature.city_id == city_id
    )
