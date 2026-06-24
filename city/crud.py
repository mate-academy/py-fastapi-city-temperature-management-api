from sqlalchemy import select
from sqlalchemy.orm import Session

from city import models, schemas


def get_cities(db: Session, skip: int = 0, limit: int = 100):
    stmt = select(models.City).offset(skip).limit(limit)
    return db.execute(stmt).scalars().all()


def get_city(db: Session, city_id: int):
    return db.get(models.City, city_id)


def create_city(db: Session, city: schemas.CityCreate):
    db_city = models.City(name=city.name, additional_info=city.additional_info)
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def update_city(db: Session, city_id: int, city: schemas.CityCreate):
    db_city = db.get(models.City, city_id)
    if db_city is None:
        return None
    db_city.name = city.name
    db_city.additional_info = city.additional_info
    db.commit()
    db.refresh(db_city)
    return db_city


def delete_city(db: Session, city_id: int):
    db_city = db.get(models.City, city_id)
    if db_city is None:
        return None
    db.delete(db_city)
    db.commit()
    return db_city
