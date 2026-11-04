from typing import Sequence, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select

from temperatures.models import Temperature


def get_temperatures(
        db: Session,
        city_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100
):
    stmt = select(Temperature)
    if city_id is not None:
        stmt = stmt.where(Temperature.city_id == city_id)

    return db.scalars(stmt.offset(skip).limit(limit)).all()


def add_temperature(db: Session, city_id: int, temp_val: float):
    new_temp = Temperature(city_id=city_id, temperature=temp_val)
    db.add(new_temp)
    db.commit()
    db.refresh(new_temp)
    return new_temp
