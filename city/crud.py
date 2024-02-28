from sqlalchemy.orm import Session

from db import models
from city import schemas


def get_city_by_name(db: Session, name: str):
    return db.query(models.DBCity).filter(models.DBCity.name == name).first()


def get_all_cities(db: Session):
    return db.query(models.DBCity).all()


def create_city(db: Session, new_city: schemas.CityCreate):
    db_city = models.DBCity(
        name=new_city.name,
        additional_info=new_city.additional_info
    )
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city
