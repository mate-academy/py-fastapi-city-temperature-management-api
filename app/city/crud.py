from sqlalchemy.orm import Session

from app.city import models, schemas


def get_city(db: Session, city_id: int):
    return db.query(models.City).filter(models.City.id == city_id).first()


def get_city_by_name(db: Session, name: str):
    return db.query(models.City).filter(models.City.name == name).first()


def get_cities(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.City).offset(skip).limit(limit).all()


def create_city(db: Session, city: schemas.CityCreate):
    db_city = models.City(**city.model_dump())
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def update_city(db: Session, db_city: models.City, city: schemas.CityCreate):
    for field, value in city.model_dump().items():
        setattr(db_city, field, value)
    db.commit()
    db.refresh(db_city)
    return db_city


def delete_city(db: Session, db_city: models.City):
    db.delete(db_city)
    db.commit()
