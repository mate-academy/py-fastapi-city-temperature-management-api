from sqlalchemy.orm import Session
from app.temperature import models, schemas


def create_temperature(db: Session, temperature: schemas.TemperatureCreate):
    db_temperature = models.Temperature(**temperature.dict())
    db.add(db_temperature)
    db.commit()
    db.refresh(db_temperature)
    return db_temperature


def get_temperatures(db: Session):
    return db.query(models.Temperature).all()


def get_temperatures_by_city_id(db: Session, city_id: int):
    return db.query(models.Temperature).filter(models.Temperature.city_id == city_id).all()
