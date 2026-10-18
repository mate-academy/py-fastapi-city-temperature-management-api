from sqlalchemy.orm import Session

import models
from temperatures import schemas


def create_temperature(db:Session, temperature: schemas.TemperatureCreate):
    db_temperature = models.Temperature(**temperature.model_dump())
    db.add(db_temperature)
    db.commit()
    db.refresh(db_temperature)
    return db_temperature


def get_temperatures(
        db:Session,
        skip: int = 0,
        limit: int = 100,
        city_id: int | None = None,
):
    query = db.query(models.Temperature)
    if city_id is not None:
        query = query.filter(models.Temperature.city_id == city_id)
    return query.offset(skip).limit(limit).all()
