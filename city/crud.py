from sqlalchemy import select
from sqlalchemy.orm import Session

import city.schemas as schemas
from city import models


def create_city(db: Session, city: schemas.CityCreate):
    db_city = models.City(name=city.name, additional_info=city.additional_info)
    db.add(db_city)
    db.commit()
    db.refresh(db_city)

    return db_city


def get_cities(
    db: Session, skip: int = 0, limit: int = 100, additional_info: str = None
):
    queryset = select(models.City)
    if additional_info is not None:
        queryset = queryset.where(models.City.additional_info == additional_info)

    queryset = queryset.offset(skip).limit(limit)
    return db.scalars(queryset).all()


def get_city_by_id(db: Session, city_id: int):
    return db.scalar(select(models.City).where(models.City.id == city_id))


def get_city_by_name(db: Session, name: str):
    return db.scalar(select(models.City).where(models.City.name == name))


def update_city(db: Session, city_id: int, city: schemas.CityUpdate):
    db.query(models.City).filter(models.City.id == city_id).update(city.dict())
    db.commit()
    return get_city_by_id(db, city_id)


def delete_city(db: Session, city_id: int):
    deleted_rows = (
        db.query(models.City)
        .filter(models.City.id == city_id)
        .delete(synchronize_session=False)
    )
    db.commit()
    return deleted_rows
