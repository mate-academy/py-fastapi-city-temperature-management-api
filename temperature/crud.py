from datetime import datetime

from sqlalchemy.orm import Session

from temperature import models


def create_temperature(
    db: Session,
    city_id: int,
    date_time: datetime,
    temperature: float,
) -> models.Temperature:
    db_temperature = models.Temperature(
        city_id=city_id,
        date_time=date_time,
        temperature=temperature,
    )
    db.add(db_temperature)
    db.commit()
    db.refresh(db_temperature)
    return db_temperature


def get_temperatures(
    db: Session,
    city_id: int | None = None,
) -> list[models.Temperature]:
    query = db.query(models.Temperature)
    if city_id is not None:
        query = query.filter(models.Temperature.city_id == city_id)
    return query.order_by(models.Temperature.date_time.desc(), models.Temperature.id.desc()).all()
