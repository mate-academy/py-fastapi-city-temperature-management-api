from sqlalchemy.orm import Session

from . import models
from . import schemas


def get_temperatures(db: Session, city_id: int | None = None):
    query = db.query(models.Temperature)

    if city_id is not None:
        query = query.filter(
            models.Temperature.city_id == city_id
        )

    return query.all()


def create_temperature(db: Session, temperature: schemas.TemperatureCreate):
    db_temperature = models.Temperature(
        city_id=temperature.city_id, temperature=temperature.temperature
    )
    db.add(db_temperature)
    db.commit()
    db.refresh(db_temperature)
    return db_temperature
