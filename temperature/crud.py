from typing import List

from sqlalchemy.orm import Session

from temperature import models, schemas
from city import models as city_models


def get_temperatures(
        db: Session, skip: int = 0, limit: int = 10
) -> List[models.Temperature]:
    return db.query(models.Temperature).offset(skip).limit(limit).all()


def get_temperature_by_city(
    db: Session, city_id: int, skip: int = 0, limit: int = 10
) -> List[models.Temperature]:
    return (
        db.query(models.Temperature)
        .filter(models.Temperature.city_id == city_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_temperature(
        db: Session, temperature: schemas.TemperatureCreate
) -> models.Temperature:
    db_temperature = models.Temperature(**temperature.dict())
    db.add(db_temperature)
    db.commit()
    db.refresh(db_temperature)
    return db_temperature


def get_cities(db: Session) -> List[city_models.City]:
    return db.query(city_models.City).all()
