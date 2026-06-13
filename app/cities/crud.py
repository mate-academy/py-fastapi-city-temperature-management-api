from sqlalchemy.orm import Session
from app.cities import models, schemas

def get_city(db: Session, city_id: int):
    return db.query(models.City).filter(models.City.id == city_id).first()

def get_city_by_name(db: Session, name: str):
    return db.query(models.City).filter(models.City.name == name).first()

def get_cities(db: Session):
    return db.query(models.City).all()

def create_city(db: Session, city: schemas.CityCreate):
    db_city = models.City(name=city.name, additional_info=city.additional_info)
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city

def update_city(db: Session, city_id: int, city_update: schemas.CityUpdate):
    db_city = get_city(db, city_id)
    if db_city:
        db_city.name = city_update.name
        db_city.additional_info = city_update.additional_info
        db.commit()
        db.refresh(db_city)
    return db_city

def delete_city(db: Session, city_id: int):
    db_city = get_city(db, city_id)
    if db_city:
        db.delete(db_city)
        db.commit()
        return True
    return False
