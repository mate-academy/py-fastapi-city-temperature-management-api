from sqlalchemy.orm import Session
from temperature import models


def get_all_temperature(db: Session):
    return db.query(models.DBTemperature).all()


def get_temperature(db: Session, temperature_id: int):
    return db.query(models.DBTemperature).filter(
        models.DBTemperature.id == temperature_id
    ).first()


def update_temperature(db: Session, city_id: int, temperature: float):
    temperature_record = db.query(models.DBTemperature).filter(
        models.DBTemperature.city_id == city_id
    ).first()

    if temperature_record:
        temperature_record.temperature = temperature
    else:
        new_temperature = models.DBTemperature(city_id=city_id, temperature=temperature)
        db.add(new_temperature)

    db.commit()
    db.refresh(temperature_record)

    return temperature_record
