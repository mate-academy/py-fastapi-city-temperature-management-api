from fastapi import HTTPException
from sqlalchemy.orm import Session

from city import models
from city import schemas


def get_all_cities(db: Session) -> list[models.City]:
    return db.query(models.City).all()


def get_city_by_id(db: Session, city_id: int) -> models.City:
    return db.query(models.City).filter(models.City.id == city_id).first()


def get_city_by_name(db: Session, name: str) -> models.City:
    return db.query(models.City).filter(models.City.name == name).first()


def create_city(db: Session, city: schemas.CityCreate) -> models.City:
    db_city = models.City(name=city.name, additional_info=city.additional_info)

    db.add(db_city)
    db.commit()
    db.refresh(db_city)

    return db_city


def update_city(db: Session, city_id: int, updated_city: schemas.CityUpdate) -> models.City:
    db_city = db.query(models.City).filter(models.City.id == city_id).first()
    if db_city:
        db_city.name = updated_city.name
        db_city.additional_info = updated_city.additional_info
        db.commit()
        db.refresh(db_city)
        return db_city

    raise HTTPException(status_code=404, detail="City not found")


def delete_city(db: Session, city_id: int) -> dict:
    db_city = db.query(models.City).filter(models.City.id == city_id).first()
    if db_city:
        db.delete(db_city)
        db.commit()
        return {"message": "City deleted"}

    raise HTTPException(status_code=404, detail="City not found")
