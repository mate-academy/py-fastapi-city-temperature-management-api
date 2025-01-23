from sqlalchemy.orm import Session
import datetime

from city_temp.city.models import City
from city_temp.temperature.models import Temperature


def create_temperature(db: Session, city: City, temperature: float):
    db_temperature = Temperature(
        city_id=city.id,
        datetime=datetime.datetime.now(datetime.timezone.utc),
        temperature=temperature,
    )
    db.add(db_temperature)
    db.commit()
    db.refresh(db_temperature)
    return db_temperature


def get_temperatures(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Temperature).offset(skip).limit(limit).all()


def get_temperatures_by_city(
    db: Session, city_id: int, skip: int = 0, limit: int = 100
):
    return (
        db.query(Temperature)
        .filter(Temperature.city_id == city_id)
        .offset(skip)
        .limit(limit)
        .all()
    )
