from sqlalchemy import select
from sqlalchemy.orm import Session

from city import models, schemas


def get_all_cities(db: Session):
    return db.scalars(select(models.DBCity)).all()


def get_specific_city(db: Session, city_id: int):
    db_city = db.scalars(
        select(models.DBCity).where(models.DBCity.id == city_id)
    ).one_or_none()
    return db_city


def update_specific_city(db: Session, city_id: int, city: schemas.CityUpdate):
    db_city = db.scalars(
        select(models.DBCity).where(models.DBCity.id == city_id)
    ).one_or_none()
    if db_city is None:
        return None
    db_city.name = city.name
    db_city.additional_info = city.additional_info

    db.commit()
    db.refresh(db_city)
    return db_city


def create_city(db: Session, city: schemas.CityCreate):
    db_city = models.DBCity(
        name=city.name, additional_info=city.additional_info
    )
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def delete_city(db: Session, city_id: int):
    db_city = db.scalars(
        select(models.DBCity).where(models.DBCity.id == city_id)
    ).one_or_none()
    if db_city is None:
        return None
    copy_db_city = schemas.City.model_validate(db_city)
    db.delete(db_city)
    db.commit()
    return copy_db_city
