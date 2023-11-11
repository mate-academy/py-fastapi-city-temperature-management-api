from datetime import datetime
from sqlalchemy.orm import Session
import asyncio

from temperature import models
from city import models as city_models
from scraper import get_city_temperature


async def create_update_temperatures(db: Session):
    all_cities = db.query(city_models.City).all()

    tasks = [get_city_temperature(city.name) for city in all_cities]

    results = await asyncio.gather(*tasks)

    db_temperatures = []
    for city, temperature in zip(all_cities, results):
        db_temperature = models.Temperature(
            city_id=city.id,
            temperature=temperature,
            date_time=datetime.now(),
        )
        db_temperatures.append(db_temperature)

    db.add_all(db_temperatures)
    db.commit()
    for db_temperature in db_temperatures:
        db.refresh(db_temperature)


def get_temperatures(
        db: Session, skip: int = 0, limit: int = 100, city_id: int = None
):
    query = db.query(models.Temperature).offset(skip).limit(limit).all()
    if city_id:
        query = (
            db.query(models.Temperature)
            .filter(models.Temperature.city_id == city_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    return query
