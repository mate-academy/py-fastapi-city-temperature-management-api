from typing import Any
from sqlalchemy.orm import Session

from app.models.temperature import DBTemperature
from app.schemas.temperature import TemperatureCreate


def create_temperature(db: Session, temp: TemperatureCreate) -> Any:
    db_temp = DBTemperature(
        date_time=temp.date_time,
        temperature=temp.temperature,
        city_id=temp.city_id
    )
    db.add(db_temp)
    db.commit()
    db.refresh(db_temp)
    return db_temp


def get_temperatures(
        db: Session,
        city_id: int | None = None,
        skip: int = 0,
        limit: int = 10
) -> Any:
    query = db.query(DBTemperature)
    if city_id is not None:
        query = query.filter(DBTemperature.city_id == city_id)
    return query.offset(skip).limit(limit).all()
