from sqlalchemy.orm import Session

from temperature_app import models
from temperature_app.schemas import TemperatureCreate


def create_temperature(
    db: Session, temperature: TemperatureCreate
) -> models.Temperature:
    db_temperature = models.Temperature(**temperature.dict())
    db.add(db_temperature)
    db.commit()
    db.refresh(db_temperature)
    return db_temperature
