from sqlalchemy.orm import Session
from schemas import cities
from db import models

def get_all_cities(db: Session):
    return db.query(models.City).all()

def get_city_by_id(db: Session, id_city: int):
    return db.query(models.City).filter(models.City.id == id_city).first()

def get_name_city(db: Session, name_city: str):
    return db.query(models.City).filter(models.City.name == name_city).first()

def create_city(db: Session, create_cities: cities.CreateCity):
    db_create_city = models.City(
        name = create_cities.name,
        additional_info = create_cities.additional_info
    )
    db.add(db_create_city)
    db.commit()
    db.refresh(db_create_city)
    return db_create_city