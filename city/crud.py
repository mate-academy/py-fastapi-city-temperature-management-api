from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models, schemas


def create_city(db: Session, city: schemas.CityCreate):
    existing_city = db.query(models.City).filter(models.City.name == city.name).first()
    if existing_city:
        raise HTTPException(
            status_code=409,
            detail=f"City with name '{city.name}' already exists"
        )
    db_city = models.City(name=city.name, additional_info=city.additional_info)
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def get_cities(db: Session):
    return db.query(models.City).all()


def get_city(db: Session, city_id: int):
    return db.query(models.City).filter(models.City.id == city_id).first()


def delete_city(db: Session, city_id: int):
    city = get_city(db, city_id)
    if city:
        db.delete(city)
        db.commit()
    return city


from fastapi import HTTPException

def update_city(db: Session, city_id: int, city_update: schemas.CityCreate):
    city = get_city(db, city_id)
    if not city:
        return None

    existing_city = db.query(models.City).filter(models.City.name == city_update.name).first()
    if existing_city and existing_city.id != city_id:
        raise HTTPException(
            status_code=409,
            detail=f"City with name '{city_update.name}' already exists"
        )

    city.name = city_update.name
    city.additional_info = city_update.additional_info
    db.commit()
    db.refresh(city)
    return city

