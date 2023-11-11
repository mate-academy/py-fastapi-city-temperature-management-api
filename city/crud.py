from sqlalchemy.orm import Session

from city import models, schemas


def create_city(db: Session, city: schemas.CityCreateUpdate):
    db_city = models.City(**city.dict())
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def get_cities(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.City).offset(skip).limit(limit).all()


def get_city(db: Session, city_id: int):
    return db.query(models.City).filter(models.City.id == city_id).first()


def update_city(db: Session, city_id: int, city: schemas.CityCreateUpdate):
    db.query(models.City).filter(models.City.id == city_id).update(city.dict())
    db.commit()
    db_city = db.query(models.City).filter(models.City.id == city_id).first()
    return db_city


def delete_city(db: Session, city_id: int):
    db.query(models.City).filter(models.City.id == city_id).delete()
    db.commit()
    return True
