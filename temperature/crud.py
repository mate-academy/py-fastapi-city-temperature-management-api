from datetime import datetime
from typing import List

from sqlalchemy.orm import Session

from temperature import models


def get_all_temperatures_with_pagination(
        db: Session,
        skip: int = 0,
        limit: int = 10,
) -> List[models.Temperature]:

    queryset = db.query(models.Temperature)

    return queryset.offset(skip).limit(limit).all()


def get_temperature_for_specific_city(db: Session, city_id: int):
    queryset = db.query(
        models.Temperature
    ).filter(models.Temperature.city_id == city_id)

    return queryset.all()


def create_temperature(
        db: Session, temp: str, city_id: int
) -> models.Temperature:

    now = datetime.now()

    db_temperature = models.Temperature(
        date_time=now,
        temperature=temp,
        city_id=city_id,
    )

    db.add(db_temperature)
    db.commit()
    db.refresh(db_temperature)

    return db_temperature
