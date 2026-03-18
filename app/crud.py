from sqlalchemy.orm import Session
from . import models, schemas


def create_city(db: Session, city: schemas.CityCreate):
    db_city = models.City(**city.dict())
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def get_cities(db: Session):
    return db.query(models.City).all()


def delete_city(db: Session, city_id: int):
    city = db.query(models.City).filter(models.City.id == city_id).first()
    if city:
        db.delete(city)
        db.commit()
    return city


def create_temperature_record(city_id: int, temp: float):
    return models.Temperature(city_id=city_id, temperature=temp)


def get_temperatures(db: Session, city_id: int | None = None):
    query = db.query(models.Temperature)
    if city_id:
        query = query.filter(models.Temperature.city_id == city_id)
    return query.all()
