from sqlalchemy.orm import Session

from city import models
from city import schemas


def get_cities(db: Session):
    return db.query(models.DBCity).all()


def get_city_by_id(db: Session, city_id: int):
    return db.query(models.DBCity).filter(models.DBCity.id == city_id).first()


def get_city_by_name(db: Session, city_name: str):
    return (
        db.query(models.DBCity).filter(models.DBCity.name == city_name).first()
    )


def update_city(db: Session, city: schemas.City):
    db_city = (
        db.query(models.DBCity).filter(models.DBCity.id == city.id).first()
    )
    db_city.name = city.name
    db_city.additional_info = city.additional_info
    db.commit()
    return db_city


def create_city(db: Session, city: schemas.CityCreate):
    db_city = models.DBCity(
        name=city.name, additional_info=city.additional_info
    )
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def delete_city(db: Session, city: models.DBCity):
    db.delete(city)
    db.commit()
