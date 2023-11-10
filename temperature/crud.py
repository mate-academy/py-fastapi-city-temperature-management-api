from datetime import datetime

from sqlalchemy.orm import Session

from temperature import models


def get_all_temperatures(db: Session):
    return db.query(models.Temperature).all()


def get_temperature_by_city_id(db: Session, city_id: int):
    return (
        db.query(models.Temperature)
        .filter(models.Temperature.city_id == city_id)
        .first()
    )


def create_temperature(
        db: Session,
        city_id: int,
        date_time: datetime,
        temperature: float
):
    db_temperature = models.Temperature(
        city_id=city_id,
        date_time=date_time,
        temperature=temperature
    )

    db.add(db_temperature)
    db.commit()
    db.refresh(db_temperature)

    return db_temperature
