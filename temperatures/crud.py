from datetime import datetime
from typing import List

from sqlalchemy.orm import Session

from dependencies import ListDep
from temperatures.models import DbTemperature
from temperatures.schemas import Temperature


def get_temperatures(commons: ListDep) -> List[Temperature]:
    db = commons["db"]
    skip = commons["skip"]
    q = commons["q"]
    limit = commons["limit"]

    query = db.query(DbTemperature)

    if q:
        query = query.filter(DbTemperature.city_id == q)

    temperatures = query.offset(skip).limit(limit).all()

    return temperatures


def create_temperature(db: Session, city_id: int, temp: float) -> Temperature:
    temperature = DbTemperature(
        city_id=city_id,
        date_time=datetime.now(),
        temperature=temp
    )
    db.add(temperature)
    db.commit()
    db.refresh(temperature)

    return temperature
