from sqlalchemy.orm import Session

from . import models
from city import schemas


def get_city_by_name(db: Session, name: str):
    return db.query(models.City).filter(models.City.name == name).first()


def get_city_by_id(db: Session, input_id: int):
    return db.query(models.City).filter(models.City.id == input_id).first()


def get_all_cities(db: Session):
    return db.query(models.City).all()


def create_city(db: Session, new_city: schemas.CityCreate):
    db_city = models.City(
        name=new_city.name,
        additional_info=new_city.additional_info
    )
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def update_city(db: Session, input_id: int, updated_city: schemas.CityCreate):
    db_city = get_city_by_id(db, input_id)
    db_city.name = updated_city.name
    db_city.additional_info = updated_city.additional_info
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def delete_city_by_id(db, input_id):
    db_city = get_city_by_id(db, input_id)
    db.delete(db_city)
    db.commit()
    return db_city
