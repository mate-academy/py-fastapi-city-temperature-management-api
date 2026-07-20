from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.temperature import Temperature


def create_temperature(
    db: Session,
    city_id: int,
    date_time: datetime,
    temperature: float,
) -> Temperature:
    record = Temperature(
        city_id=city_id,
        date_time=date_time,
        temperature=temperature,
    )
    db.add(record)
    return record


def get_temperatures(
    db: Session,
    city_id: int | None = None,
) -> list[Temperature]:
    statement = select(Temperature)

    if city_id is not None:
        statement = statement.where(Temperature.city_id == city_id)

    statement = statement.order_by(Temperature.date_time.desc())
    return list(db.scalars(statement).all())
