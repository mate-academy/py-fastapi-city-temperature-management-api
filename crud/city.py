from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
import models
import schemas


def create_city(db: Session, city: schemas.CityCreate):
    db_city = models.City(**city.dict())
    try:
        db.add(db_city)
        db.commit()
        db.refresh(db_city)
        return db_city
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="City already exists")


def get_cities(db: Session):
    return db.query(models.City).all()


def get_city(db: Session, city_id: int):
    return db.query(models.City).filter(models.City.id == city_id).first()


def update_city(db: Session, city_id: int, city: schemas.CityUpdate):
    db_city = get_city(db=db, city_id=city_id)
    if db_city is None:
        return None
    update_data = city.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_city, key, value)
    db.commit()
    db.refresh(db_city)
    return db_city


def delete_city(db: Session, db_city: models.City):
    db.delete(db_city)
    db.commit()
    return db_city
