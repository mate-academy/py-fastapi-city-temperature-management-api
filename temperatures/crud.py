from sqlalchemy.orm import Session
from sqlalchemy import select

from .models import Temperature


def create_temperature(db: Session, city_id: int, temperature: float):
    db_temperature = Temperature(
        city_id=city_id,
        temperature=temperature
    )

    db.add(db_temperature)
    db.commit()
    db.refresh(db_temperature)

    return db_temperature


def get_temperatures(db: Session, city_id: int | None = None):
    stmt = select(Temperature)
    if city_id is not None:
        stmt = stmt.where(Temperature.city_id == city_id)

    stmt = stmt.order_by(Temperature.date_time.desc())

    return db.scalars(stmt).all()
