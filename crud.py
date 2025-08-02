from sqlalchemy.orm import Session
import models

def create_city(db: Session, city: schemas.CityCreate):
    db_city = models.DBCity(**city.dict())
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city

def get_cities(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.DBCity).offset(skip).limit(limit).all()

def get_city(db: Session, city_id: int):
    return db.query(models.DBCity).filter(models.DBCity.id == city_id).first()

def delete_city(db: Session, city_id: int):
    db_city = get_city(db, city_id)
    if not db_city:
        return None
    db.delete(db_city)
    db.commit()
    return db_city

def create_temperature(db: Session, temperature: schemas.TemperatureCreate):
    db_temp = models.DBTemperature(**temperature.dict())
    db.add(db_temp)
    db.commit()
    db.refresh(db_temp)
    return db_temp

def get_temperatures(db: Session, city_id: int = None):
    query = db.query(models.DBTemperature)
    if city_id:
        query = query.filter(models.DBTemperature.city_id == city_id)
    return query.all()
