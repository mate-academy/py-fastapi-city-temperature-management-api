import datetime

from sqlalchemy.orm import Session

from temperature import models, schemas


def get_all_temperatures(
    db: Session, skip: int, limit: int, city_id: int = None
) -> list[models.Temperature]:
    queryset = db.query(models.Temperature)
    if city_id is not None:
        queryset = queryset.filter(models.Temperature.city_id == city_id)

    return queryset.offset(skip).limit(limit).all()


def get_temperature_by_city_id(
    db: Session, city_id: int
) -> models.Temperature:
    return (
        db.query(models.Temperature)
        .filter(models.Temperature.city_id == city_id)
        .first()
    )


def create_temperature(
    db: Session,
    temp: float,
    city_id: int,
) -> models.Temperature:
    db_temp = models.Temperature(
        temperature=temp,
        city_id=city_id,
        date_time=datetime.datetime.now(),
    )

    db.add(db_temp)
    db.commit()
    db.refresh(db_temp)

    return db_temp


def update_temperature(
    db: Session,
    city_id: int,
    temp: float,
) -> models.Temperature:
    db_temp = (
        db.query(models.Temperature)
        .filter(models.Temperature.city_id == city_id)
        .first()
    )
    if db_temp:
        db_temp.temp = temp
        db_temp.date_time = datetime.datetime.now()
        db.commit()
        db.refresh(db_temp)
        return db_temp
