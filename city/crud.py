from sqlalchemy.orm import Session

from city import models
from city import schemas


def get_all_cities(
        db: Session,
        skip: int = 0,
        limit: int = 5
):
    return db.query(models.City).offset(skip).limit(limit).all()


def get_city_by_id(db: Session, id: int):
    return db.query(models.City).filter(models.City.id == id).first()


def get_city_by_name(db: Session, name: str):
    return db.query(models.City).filter(models.City.name == name).first()


def create_city(db: Session, city: schemas.CityCreate):
    db_city = models.City(**city.model_dump())
    db.add(db_city)
    db.commit()
    db.refresh(db_city)

    return db_city


def update_city(db: Session, city_id: int, city: schemas.CityCreate):
    db_city = db.query(models.City).filter(models.City.id == city_id).first()
    if db_city:
        for attr, value in city.model_dump().items():
            setattr(db_city, attr, value)
        db.commit()
        db.refresh(db_city)
    return db_city


def delete_city(db: Session, city_id: int):
    city = db.query(models.City).filter(models.City.id == city_id).first()
    if city:
        db.delete(city)
        db.commit()
    return city
