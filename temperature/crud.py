from sqlalchemy.orm import Session
from city.models import DBTemperature


def get_all_temperature(db: Session):
    return db.query(DBTemperature).all()


def get_temperature(db: Session, temperature_id: int):
    return db.query(DBTemperature).filter(DBTemperature.id == temperature_id).first()


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
