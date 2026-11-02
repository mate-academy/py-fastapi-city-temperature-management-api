import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from models import Temperature
from schemas.temperature import TemperatureCreate


def get_temperatures(
    db: Session,
    city_id: int | None = None,
    skip: int = 0,
    limit: int = 100,
) -> list[Temperature]:
    query = select(Temperature).order_by(Temperature.date_time.desc())
    if city_id is not None:
        query = query.where(Temperature.city_id == city_id)
    return list(db.scalars(query.offset(skip).limit(limit)))


def create_temperatures(
    db: Session, temperatures: list[TemperatureCreate]
) -> list[Temperature]:
    db_temperatures = [Temperature(**t.model_dump()) for t in temperatures]
    db.add_all(db_temperatures)
    db.commit()
    for db_temperature in db_temperatures:
        db.refresh(db_temperature)
    return db_temperatures
