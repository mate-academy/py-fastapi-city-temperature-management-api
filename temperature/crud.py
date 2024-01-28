from sqlalchemy.orm import Session
from city.models import DBTemperature, DBCity
from fastapi import HTTPException


def get_all_temperature(db: Session):
    return db.query(DBTemperature).all()


def get_temperature(db: Session, temperature_id: int):
    temperature = db.query(DBTemperature).filter(DBTemperature.id == temperature_id).first()

    if temperature is None:
        raise HTTPException(status_code=404, detail="Temperature not found")

    return temperature


def get_temperature_by_city_name(db: Session, city_id: int):
    city = db.query(DBCity).filter(DBCity.id == city_id).first()
    if city is None:
        raise HTTPException(status_code=404, detail="Temperature not found")

    return db.query(DBTemperature).filter(DBTemperature.city_id == city.id).first()


def update_temperature(db: Session, city_id: int, temperature: float):
    temperature_record = db.query(DBTemperature).filter(DBTemperature.city_id == city_id).first()

    if temperature_record:
        temperature_record.temperature = temperature
    else:
        new_temperature = DBTemperature(city_id=city_id, temperature=temperature)
        db.add(new_temperature)

    db.commit()
    db.refresh(temperature_record)

    return temperature_record
