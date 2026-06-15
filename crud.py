from sqlalchemy.orm import Session
import models
import schemas


def get_cities(db: Session):
    return db.query(models.City).all()

def create_city(db: Session, city: schemas.CityCreate):
    db_city = models.City(name=city.name,
                          additional_info=city.additional_info)
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city

def get_temperatures(db: Session):
    return db.query(models.Temperature).all()

def get_temperature(db: Session, city_id: int = None):
    if city_id:
        return db.query(models.Temperature).filter(models.Temperature.city_id == city_id).all()
    return db.query(models.Temperature).all()

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
