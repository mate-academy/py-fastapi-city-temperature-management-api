from sqlalchemy.orm import Session
from models.models import Temperature
from schemas.schemas import TemperatureCreate


def get_temperatures(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Temperature).offset(skip).limit(limit).all()


def create_temperature(db: Session, temperature: TemperatureCreate):
    db_temperature = Temperature(
        city_id=temperature.city_id,
        date_time=temperature.date_time,
        temperature=temperature.temperature
    )
    db.add(db_temperature)
    db.commit()
    db.refresh(db_temperature)
    return db_temperature
