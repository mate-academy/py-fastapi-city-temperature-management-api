from sqlalchemy.orm import Session
from app import models, schemas

def create_city(db: Session, city: schemas.CityCreate):
    db_city = models.City(**city.dict())
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
