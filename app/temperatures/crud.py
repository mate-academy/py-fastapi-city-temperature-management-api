import datetime
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List, Optional
from app.temperatures import models


def create_temperature(
    db: Session, city_id: int, temperature: float
) -> models.Temperature:
    db_temp = models.Temperature(
        city_id=city_id,
        temperature=temperature,
        date_time=datetime.datetime.utcnow(),
    )
    db.add(db_temp)
    return db_temp


def get_temperatures(
    db: Session, city_id: Optional[int] = None
) -> List[models.Temperature]:
    stmt = select(models.Temperature)
    if city_id is not None:
        stmt = stmt.where(models.Temperature.city_id == city_id)
    return list(db.scalars(stmt).all())
