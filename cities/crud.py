from sqlalchemy.orm import Session

from . import models, schemas

def get_all_сities(db: Session, skip: int, limit: int):
    return db.query(models.City).offset(skip).limit(limit).all()

def get_all_cities_no_pagination(db: Session):
    return db.query(models.City).all()
def get_city_by_id(db: Session, city_id: int):
    return db.query(models.City).filter(models.City.id == city_id).first()

def update_city(db: Session, city: schemas.CityCreateSchema, city_id: int):
    db_city = get_city_by_id(db, city_id=city_id)
    if db_city:
        db_city.name = city.name
        db_city.additional_info = city.additional_info
        db.commit()
        db.refresh(db_city)
    return db_city

def create_city(db: Session, city: schemas.CityCreateSchema):
    db_city = models.City(name = city.name, additional_info = city.additional_info)
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city

def delete_city(db: Session, city_id: int):
    db_city = get_city_by_id(db, city_id=city_id)
    if db_city:
        db.delete(db_city)
        db.commit()
    return db_city