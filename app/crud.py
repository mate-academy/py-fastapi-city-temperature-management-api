from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app import models, schemas


def get_city_by_name(db: Session, name: str) -> models.City | None:
    return db.query(models.City).filter(models.City.name == name).first()


def get_city(db: Session, city_id: int) -> models.City | None:
    return db.query(models.City).filter(models.City.id == city_id).first()


def list_cities(db: Session) -> list[models.City]:
    return db.query(models.City).order_by(models.City.id).all()


def create_city(db: Session, city_in: schemas.CityCreate) -> models.City:
    city = models.City(name=city_in.name, additional_info=city_in.additional_info)
    db.add(city)
    db.commit()
    db.refresh(city)
    return city


def delete_city(db: Session, city: models.City) -> None:
    db.delete(city)
    db.commit()


def list_temperatures(
    db: Session,
    city_id: int | None = None,
) -> list[models.Temperature]:
    query = db.query(models.Temperature)

    if city_id is not None:
        query = query.filter(models.Temperature.city_id == city_id)

    return query.order_by(models.Temperature.date_time.desc()).all()

def create_temperature(
    db: Session,
    city_id: int,
    temperature: float,
) -> models.Temperature:
    temp = models.Temperature(
        city_id=city_id,
        temperature=temperature,
        date_time=datetime.now(timezone.utc),
    )
    db.add(temp)
    db.commit()
    db.refresh(temp)
    return temp