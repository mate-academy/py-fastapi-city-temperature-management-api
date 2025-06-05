from sqlalchemy.orm import Session
from app.city import models, schemas


def get_cities(db: Session):
    return db.query(models.City).all()


def get_city(db: Session, id_city: int):
    return db.query(models.City).filter(models.City.id == id_city).first()


def create_city(db: Session, city: schemas.CityCreate):
    db_city = models.City(
        name=city.name,
        additional_info=city.additional_info,
    )
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def delete_city(db: Session, id_city: int):
    city = db.query(models.City).filter(models.City.id == id_city).first()
    if city:
        db.delete(city)
        db.commit()
    return city
