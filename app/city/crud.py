from sqlalchemy import select
from sqlalchemy.orm import Session

from . import models, schemas


def get_all_cities(db: Session):
    return db.scalars(select(models.City)).all()


def get_one_city(db: Session, city_id: int):
    return db.scalars(select(models.City).where(models.City.id == city_id)).first()


def get_city_by_name(db: Session, city_name: str):
    return db.scalars(select(models.City).where(models.City.name == city_name)).first()


def update_city(db: Session, city_id: int, city_data: schemas.CityUpdate):
    db_city = get_one_city(db, city_id)

    if not db_city:
        return None

    if city_data.name is not None:
        db_city.name = city_data.name

    if city_data.additional_info is not None:
        db_city.additional_info = city_data.additional_info

    db.commit()
    db.refresh(db_city)
    return db_city


def create_city(db: Session, city: schemas.CityCreate):
    db_city = models.City(
        name=city.name,
        additional_info=city.additional_info,
    )
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def delete_city(db: Session, city_id: int):
    db_city = get_one_city(db, city_id)

    if not db_city:
        return None

    db.delete(db_city)
    db.commit()
    return db_city
