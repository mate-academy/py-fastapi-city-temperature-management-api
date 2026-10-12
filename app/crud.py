from sqlalchemy.orm import Session
from app import models, schemas
from datetime import datetime

def create_city(db: Session, city: schemas.CityCreate) -> models.City:
    db_city = models.City(
        name=city.name,
        additional_info=city.additional_info
    )

    db.add(db_city)
    db.commit()
    db.refresh(db_city)

    return db_city

def get_cities(db: Session) -> list[models.City]:
    return db.query(models.City).all()

def get_city_by_id(db: Session, city_id: int) -> models.City | None:
    return db.query(models.City).filter(models.City.id == city_id).first()


def update_city(
    db: Session,
    city_id: int,
    city: schemas.CityCreate,
) -> models.City | None:
    db_city = get_city_by_id(db=db, city_id=city_id)

    if db_city is None:
        return None

    db_city.name = city.name
    db_city.additional_info = city.additional_info

    db.commit()
    db.refresh(db_city)

    return db_city

def delete_city(db: Session, city_id: int) -> models.City | None:
    db_city = get_city_by_id(db=db, city_id=city_id)

    if db_city is None:
        return None

    db.delete(db_city)
    db.commit()

    return db_city

def create_temperature(db: Session, city_id: int, temperature: float) -> models.Temperature:
    db_temperature = models.Temperature(
        city_id=city_id,
        date_time=datetime.now(),
        temperature=temperature,
    )

    db.add(db_temperature)
    db.commit()
    db.refresh(db_temperature)

    return db_temperature

def get_temperatures(db: Session, city_id: int | None = None) -> list[models.Temperature]:

    query = db.query(models.Temperature)

    if city_id is not None:
        query = query.filter(models.Temperature.city_id == city_id)

    return query.all()