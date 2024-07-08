from sqlalchemy.orm import Session

from . import models, schemas


def get_city_by_id(db: Session, city_id: int) -> models.DBCity:
    return db.query(models.DBCity).filter(models.DBCity.id == city_id).first()


def get_cities_list(db: Session) -> list[models.DBCity]:
    return db.query(models.DBCity).all()


def create_city(db: Session, city: schemas.CityCreate) -> models.DBCity:
    db_city = models.DBCity(
        name=city.name,
        additional_info=city.additional_info,
    )
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def update_city_by_id(db: Session, city_id: int,  city: schemas.CityUpdate) -> models.DBCity:
    db_city = get_city_by_id(db=db, city_id=city_id)
    if city.name:
        db_city.name = city.name
    if city.additional_info:
        db_city.additional_info = city.additional_info
    db.commit()
    db.refresh(db_city)
    return db_city


def delete_city_by_id(db: Session, city_id: int) -> models.DBCity:
    db_city = get_city_by_id(db=db, city_id=city_id)
    db.delete(db_city)
    db.commit()
    return db_city
