from sqlalchemy.orm import Session

from . import models, schemas


def create_temperature(db: Session,
                       temperature: schemas.TemperatureCreate,
                       ) -> models.DBTemperature:
    db_temperature = schemas.Temperature(**temperature.model_dump())
    db.add(db_temperature)
    db.commit()
    db.refresh(db_temperature)

    return db_temperature


def get_all_temperatures(db: Session,
                         ) -> list[models.DBTemperature]:
    return (db
            .query(models.DBTemperature)
            .all()
            )


def get_temperatures_by_city(db: Session,
                             city_id: int,
                             ) -> list[models.DBTemperature]:
    return (db
            .query(models.DBTemperature)
            .filter(models.DBTemperature.city_id == city_id)
            .all()
            )
