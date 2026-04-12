from datetime import datetime
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from models import Temperature


def create_temperature(
        db: Session,
        city_id: int,
        temperature: float,
        date_time: datetime,
) -> Temperature:
    db_temperature = Temperature(
        city_id=city_id,
        date_time=date_time,
        temperature=temperature,
    )

    db.add(db_temperature)
    db.commit()
    db.refresh(db_temperature)
    return db_temperature

def get_temperature(
        db: Session,
        city_id: int | None=None
) -> Sequence[Temperature]:
    stmt = select(Temperature)

    if city_id is not None:
        stmt = stmt.where(Temperature.city_id == city_id)
    result = db.scalars(stmt).all()
    return result
