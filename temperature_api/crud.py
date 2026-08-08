from sqlalchemy.orm import Session

from temperature_api import models


def get_all_temperatures(db: Session):
    statement = db.query(models.Temperature)
    return list(db.scalars(statement).all())


def get_temperature_for_city(db: Session, city_id: int):
    statement = db.query(models.Temperature).filter(models.Temperature.city_id == city_id)
    return list(db.scalars(statement).all())

