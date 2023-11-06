from datetime import datetime
from sqlalchemy.orm import Session

from temperature import models
from city import models
from scraper import get_city_temperature


def create_update_temperatures(db: Session):
    all_cities = db.query(models.City).all()
    for city in all_cities:
        city_temperature = get_city_temperature(city.name)
        db_temperature = models.Temperature(
            city_id=city.id,
            temperature=city_temperature,
            date_time=datetime.now(),
        )
        db.add(db_temperature)
        db.commit()
        db.refresh(db_temperature)


def get_temperatures(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        city_id: int = None
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
