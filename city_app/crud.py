from fastapi import HTTPException
from sqlalchemy.orm import Session

from city_app import models, schemas


def get_cities(db: Session):
    return db.query(models.City).all()


def get_city(db: Session, city_id: int):
    city = db.query(models.City).filter(models.City.id == city_id).first()

    if city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return city


def create_city(db: Session, city: schemas.CityCreate):
    db_city = models.City(name=city.name, additional_info=city.additional_info)
    db.add(db_city)
    db.commit()
    db.refresh(db_city)

    return db_city


def update_city(db: Session, city_id: int, city: schemas.CityCreate):
    db_city = db.query(models.City).filter(models.City.id == city_id).first()

    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    db_city.name = city.name
    db_city.additional_info = city.additional_info
    db.commit()
    db.refresh(db_city)

    return db_city


def delete_city(db: Session, city_id: int):
    db_city = db.query(models.City).filter(models.City.id == city_id).first()

    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    db.delete(db_city)
    db.commit()

    return db_city
