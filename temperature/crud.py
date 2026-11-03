from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from temperature import models, schemas


def get_all_temperatures(
    db: Session, city_id: int | None = None
) -> Sequence[models.DBTemperature]:
    queryset = select(models.DBTemperature).order_by(
        models.DBTemperature.date_time
    )

    if city_id is not None:
        queryset = queryset.where(models.DBTemperature.city_id == city_id)

    return db.scalars(queryset).all()


def create_temperatures(
    db: Session, temperatures: list[schemas.TemperatureCreate]
) -> list[models.DBTemperature]:
    db_temperatures = [
        models.DBTemperature(
            city_id=temperature.city_id,
            temperature=temperature.temperature,
        )
        for temperature in temperatures
    ]

    db.add_all(db_temperatures)
    db.commit()

    for db_temperature in db_temperatures:
        db.refresh(db_temperature)

    return db_temperatures
