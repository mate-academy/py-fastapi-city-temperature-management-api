from sqlalchemy import select
from sqlalchemy.orm import Session

from temperature import models, schemas


def get_temperatures(db: Session, skip: int = 0, limit: int = 100, city_id: int | None = None):
    stmt = select(models.Temperature)
    if city_id is not None:
        stmt = stmt.where(models.Temperature.city_id == city_id)
    stmt = stmt.offset(skip).limit(limit)
    return db.execute(stmt).scalars().all()


def create_temperature(db: Session, temperature: schemas.TemperatureBase):
    db_temp = models.Temperature(
        city_id=temperature.city_id,
        date_time=temperature.date_time,
        temperature=temperature.temperature,
    )
    db.add(db_temp)
    db.commit()
    db.refresh(db_temp)
    return db_temp
