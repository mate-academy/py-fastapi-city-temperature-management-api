from sqlalchemy.orm import Session
import models
import schemas


def get_cities(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.City).offset(skip).limit(limit).all()

def create_city(db: Session, city: schemas.CityCreate):
    db_city = models.City(name=city.name,
                          additional_info=city.additional_info)
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city

def get_temperatures(db: Session, skip: int = 0, limit: int = 100, city_id: int = None):
    query = db.query(models.Temperature)
    if city_id is not None:
        query = query.filter(models.Temperature.city_id == city_id)
    return query.offset(skip).limit(limit).all()

def create_temperature(db: Session, temp: schemas.TemperatureCreate):
    db_temp = models.Temperature(**temp.model_dump())
    db.add(db_temp)
    db.commit()
    db.refresh(db_temp)
    return db_temp

def delete_city(db: Session, city_id: int):
    db_city = db.query(models.City).filter(models.City.id == city_id).first()
    if db_city:
        db.delete(db_city)
        db.commit()
    return db_city
