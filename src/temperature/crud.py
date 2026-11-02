from sqlalchemy import select
from sqlalchemy.orm import Session

from src.temperature.models import Temperature
from src.temperature.schemas import TemperatureCreate


def get_temperatures(
    db: Session,
    city_id: int | None = None,
    skip: int = 0,
    limit: int = 100,
) -> list[Temperature]:
    stmt = select(Temperature)
    if city_id is not None:
        stmt = stmt.where(Temperature.city_id == city_id)
    stmt = stmt.order_by(Temperature.date_time.desc()).offset(skip).limit(limit)
    return list(db.scalars(stmt).all())


def create_temperatures(db: Session, temperatures: list[TemperatureCreate]) -> list[Temperature]:
    db_temperatures = [Temperature(**t.model_dump()) for t in temperatures]
    db.add_all(db_temperatures)
    db.commit()
    return db_temperatures
