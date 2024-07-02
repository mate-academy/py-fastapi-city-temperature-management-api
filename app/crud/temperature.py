from sqlalchemy.orm import Session

from app.models import TemperatureModel
from app.schemas import TemperatureCreate


def get_temperature(db: Session, temperature_id: str):
    return db.query(TemperatureModel).filter(
        TemperatureModel.id == temperature_id
        ).first()


def get_temperatures(db: Session, skip: int = 0, limit: int = 10):
    return db.query(TemperatureModel).offset(skip).limit(limit).all()


def get_temperatures_by_city(db: Session, city_id: str):
    return db.query(TemperatureModel).filter(
        TemperatureModel.city_id == city_id
        ).all()


def create_temperature(db: Session, temperature: TemperatureCreate):
    db_temperature = TemperatureModel(**temperature.dict())
    db.add(db_temperature)
    db.commit()
    db.refresh(db_temperature)
    return db_temperature
