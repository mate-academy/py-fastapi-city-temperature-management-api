from datetime import datetime
from typing import Optional, List

from sqlalchemy.orm import Session

from app import models, schemas


def create_city(
    db: Session,
    city: schemas.CityCreate
) -> models.City:
    city = models.City(
        name=city.name,
        additional_info=city.additional_info
    )
    db.add(city)
    db.commit()
    db.refresh(city)
    return city


def get_city(
    db: Session,
    city_id: int
) -> Optional[models.City]:
    return db.query(models.City).filter(models.City.id == city_id).first()


def get_city_by_name(
    db: Session,
    name: str
) -> Optional[models.City]:
    return db.query(models.City).filter(models.City.name == name).first()


def list_cities(db: Session) -> List[models.City]:
    return db.query(models.City).all()


def update_city(
    db: Session,
    city_id: int,
    city_update: schemas.CityUpdate
) -> Optional[models.City]:
    city = get_city(db, city_id)
    if not city:
        return None
    if city_update.name is not None:
        city.name = city_update.name
    if city_update.additional_info is not None:
        city.additional_info = city_update.additional_info
    db.add(city)
    db.commit()
    db.refresh(city)
    return city


def delete_city(
    db: Session,
    city_id: int
) -> bool:
    db_city = get_city(db, city_id)
    if not db_city:
        return False
    db.delete(db_city)
    db.commit()
    return True


def create_temperature(
    db: Session,
    city_id: int,
    temperature_value: float,
    date_time: Optional[datetime] = None
) -> models.Temperature:
    if date_time is None:
        date_time = datetime.utcnow()
    db_temp = models.Temperature(
        city_id=city_id,
        temperature=temperature_value,
        date_time=date_time
    )
    db.add(db_temp)
    db.commit()
    db.refresh(db_temp)
    return db_temp


def list_temperatures(
    db: Session,
    city_id: Optional[int] = None
) -> List[models.Temperature]:
    q = db.query(models.Temperature)
    if city_id is not None:
        q = q.filter(models.Temperature.city_id == city_id)
    return q.order_by(models.Temperature.date_time.desc()).all()
