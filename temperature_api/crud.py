from sqlalchemy import select
from sqlalchemy.orm import Session

from temperature_api import models


def get_all_temperatures(db: Session):
    statement = select(models.Temperature)
    return list(db.scalars(statement).all())


def get_temperature_for_city(db: Session, city_id: int):
    statement = select(models.Temperature).where(models.Temperature.city_id == city_id)
    return list(db.scalars(statement).all())


def create_temperature(
    db: Session,
    city_id: int,
    temperature_value: float,
) -> models.Temperature:
    db_temperature = models.Temperature(
        city_id=city_id,
        temperature=temperature_value,
    )

    db.add(db_temperature)
    db.commit()
    db.refresh(db_temperature)

    return db_temperature
