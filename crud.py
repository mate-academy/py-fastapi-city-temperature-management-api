from sqlalchemy.orm import Session
import models, schemas


def get_cities(db: Session):
    return db.query(models.City).all()

def get_city(db: Session, city_id: int):
    return db.query(models.City).filter(models.City.id == city_id).first()

def create_city(db: Session, city: schemas.CityCreate):
    db_city = models.City(**city.model_dump())
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city

def delete_city(db: Session, city_id: int):
    db_city = db.query(models.City).filter(models.City.id == city_id).first()
    if db_city:
        db.delete(db_city)
        db.commit()
    return db_city

def create_temperature(db: Session, city_id: int, temp: float):
    db_temp = models.Temperature(city_id=city_id, temperature=temp)
    db.add(db_temp)
    db.commit()
    return db_temp

def get_temperatures(db: Session, city_id: int = None):
    query = db.query(models.Temperature)
    if city_id:
        query = query.filter(models.Temperature.city_id == city_id)
    return query.all()
