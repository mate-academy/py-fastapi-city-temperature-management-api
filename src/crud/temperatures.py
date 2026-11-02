from typing import List

import schemas

from sqlalchemy import select
from sqlalchemy.orm import Session

from db import models


def get_all_temperatures(db: Session) -> List[models.Temperature]:
    return list(db.scalars(select(models.Temperature)).all())


def get_temperatures_by_city_id(
    db: Session, city_id: int
) -> List[models.Temperature]:
    return list(
        db.scalars(
            select(models.Temperature).where(
                models.Temperature.city_id == city_id
            )
        ).all()
    )


def create_temperature(
    db: Session, temperature_data: schemas.TemperatureCreate
) -> models.Temperature:
    db_temperature = models.Temperature(**temperature_data.model_dump())
    db.add(db_temperature)
    db.commit()
    db.refresh(db_temperature)
    return db_temperature
