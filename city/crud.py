from fastapi import HTTPException
from sqlalchemy.orm import Session


from . import models
from . import schemas


def get_city_by_id(db: Session, city_id: int):
    db_city = db.query(models.City).filter(models.City.id == city_id).first()

    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return db_city


def get_all_cities(db: Session):
    return db.query(models.City).all()


def create_city(db: Session, city: schemas.CityCreate):
    db_city = models.City(
        name=city.name,
        additional_info=city.additional_info
    )
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def delete_city(db: Session, city_id: int):
    db_city = get_city_by_id(db, city_id)
    db.delete(db_city)
    db.commit()


def put_city(db: Session, city: schemas.CityCreate, city_id: int):
    db_city = get_city_by_id(db, city_id)
    db_city.name = city.name
    db_city.additional_info = city.additional_info
    db.commit()
    return db_city
