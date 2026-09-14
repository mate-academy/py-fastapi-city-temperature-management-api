from sqlalchemy.orm import Session
from Temperature import schemas, models


def get_all_city(db: Session):
    return db.query(models.DBCity).all()


def get_all_temperature(db: Session):
    return db.query(models.DBTemperature).all()


def get_temperature_by_city_id(db: Session, city_id: int):
    return db.query(
        models.DBTemperature
    ).filter(models.DBTemperature.city_id == city_id).all()


def update_temperature_city(
        db: Session,
        temperature: schemas.TemperatureAdded,
):
    db_temperature_add = models.DBTemperature(
        city_id=temperature.city_id,
        date_time=temperature.date_time,
        temperature=temperature.temperature
    )
    db.add(db_temperature_add)
    db.commit()
    db.refresh(db_temperature_add)

    return db_temperature_add
