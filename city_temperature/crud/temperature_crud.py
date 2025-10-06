from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from city_temperature.models.temperature import Temperature
from city_temperature.schemas.temperature import TemperatureCreate
from typing import List, Optional


def create_temperature(db: Session, temperature: TemperatureCreate) -> Optional[Temperature]:
    db_temp = Temperature(
        city_id=temperature.city_id,
        temperature=temperature.temperature
    )
    try:
        db.add(db_temp)
        db.commit()
        db.refresh(db_temp)
        return db_temp
    except IntegrityError:
        db.rollback()
        return None


def get_all_temperatures(db: Session) -> List[Temperature]:
    return db.query(Temperature).all()


def get_temperatures_by_city(db: Session, city_id: int) -> List[Temperature]:
    return db.query(Temperature).filter(Temperature.city_id == city_id).all()
