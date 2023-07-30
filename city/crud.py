from datetime import datetime

from sqlalchemy.orm import Session

from city import schemas, models


def create_city(db: Session, city: schemas.CityCreate):
    db_city = models.City(name=city.name, additional_info=city.additional_info)
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def get_cities(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.City).offset(skip).limit(limit).all()


def get_city(db: Session, city_id: int):
    return db.query(models.City).filter(models.City.id == city_id).first()


def update_city(db: Session, db_city: models.City, city: schemas.CityCreate):
    for key, value in city.model_dump().items():
        setattr(db_city, key, value)
    db.commit()
    return db_city


def delete_city(db: Session, db_city: models.City):
    db.delete(db_city)
    db.commit()
    return f"City has been successfully deleted"


def create_temperature(
    db: Session, city_id: int, date_time: datetime, temperature: float
):
    db_temp = models.Temperature(
        city_id=city_id, date_time=date_time, temperature=temperature
    )
    db.add(db_temp)
    db.commit()
    db.refresh(db_temp)
    return db_temp


def get_temperature_records(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Temperature).offset(skip).limit(limit).all()


def get_specific_city_temperature_records(db: Session, city_id: int):
    return db.query(models.Temperature).filter(models.Temperature.city_id == city_id)
