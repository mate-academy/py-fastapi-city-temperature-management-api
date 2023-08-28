from sqlalchemy.orm import Session

from models import TemperatureDB
from schemas import TemperatureCreate


def create_temperature(db: Session, temperature: TemperatureCreate):
    db_temperature = TemperatureDB(
        city_id=temperature.city_id,
        date_time=temperature.date_time,
        temperature=temperature.temperature,
    )
    db.add(db_temperature)
    db.commit()
    db.refresh(db_temperature)

    return db_temperature


def read_all_temperatures(
    db: Session, city_id: int | None = None, skip: int = 0, limit: int = 10
):
    queryset = db.query(TemperatureDB)

    if city_id is not None:
        queryset = queryset.filter(TemperatureDB.city_id == city_id)

    return queryset.offset(skip).limit(limit).all()
