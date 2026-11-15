from datetime import datetime

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import models, schemas


def get_city(db: Session, city_id: int) -> models.City | None:
    return db.get(models.City, city_id)


def get_city_by_name(db: Session, name: str) -> models.City | None:
    statement = select(models.City).where(models.City.name == name)
    return db.execute(statement).scalar_one_or_none()


def get_cities(db: Session) -> list[models.City]:
    statement = select(models.City).order_by(models.City.id)
    return list(db.execute(statement).scalars().all())


def create_city(db: Session, city_in: schemas.CityCreate) -> models.City:
    city = models.City(name=city_in.name, additional_info=city_in.additional_info)
    db.add(city)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise
    db.refresh(city)
    return city


def update_city(
    db: Session,
    city: models.City,
    city_in: schemas.CityUpdate,
) -> models.City:
    data = city_in.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(city, field, value)
    db.add(city)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise
    db.refresh(city)
    return city


def delete_city(db: Session, city: models.City) -> None:
    db.delete(city)
    db.commit()


def get_temperatures(
    db: Session,
    city_id: int | None = None,
) -> list[models.Temperature]:
    statement = select(models.Temperature).order_by(models.Temperature.date_time.desc())
    if city_id is not None:
        statement = statement.where(models.Temperature.city_id == city_id)
    return list(db.execute(statement).scalars().all())


def create_temperature(
    db: Session,
    city_id: int,
    date_time: datetime,
    temperature: float,
) -> models.Temperature:
    record = models.Temperature(
        city_id=city_id,
        date_time=date_time,
        temperature=temperature,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def create_temperatures(
    db: Session,
    records: list[tuple[int, datetime, float]],
) -> list[models.Temperature]:
    created: list[models.Temperature] = []
    for city_id, date_time, temperature in records:
        record = models.Temperature(
            city_id=city_id,
            date_time=date_time,
            temperature=temperature,
        )
        db.add(record)
        created.append(record)
    db.commit()
    for record in created:
        db.refresh(record)
    return created
