from typing import List
from sqlalchemy.orm import Session
from temperature import models
from temperature import schemas


def create_temperature(
        db: Session,
        temperature: schemas.TemperetureCreate
) -> schemas.Tempereture:
    temp_record = models.Temperature(
        city_id=temperature.city_id,
        temperature=temperature.temperature,
    )
    db.add(temp_record)
    db.commit()
    db.refresh(temp_record)
    return temp_record


def get_all_temperatures(
        db: Session,
        skip: int = 0,
        limit: int = 10
) -> List[schemas.Tempereture]:
    return db.query(models.Temperature).order_by(
        models.Temperature.date_time.desc()
    ).offset(skip).limit(limit).all()


def get_temperatures_by_city(
        db: Session,
        city_id: int,
        skip: int = 0,
        limit: int = 10
) -> List[schemas.Tempereture]:
    return db.query(models.Temperature).filter(
        models.Temperature.city_id == city_id
    ).order_by(
        models.Temperature.date_time.desc()
    ).offset(skip).limit(limit).all()
