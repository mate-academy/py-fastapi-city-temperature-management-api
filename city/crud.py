from sqlalchemy.orm import Session
from typing import List
from city import models, schemas


def get_all_cities(
        db: Session,
) -> List[models.City]:

    return db.query(models.City).all()


def get_all_cities_with_pagination(
        db: Session,
        skip: int = 0,
        limit: int = 10,
) -> List[models.City]:

    queryset = db.query(models.City)

    return queryset.offset(skip).limit(limit).all()


def get_city_by_id(db: Session, city_id: int) -> models.City:

    return db.query(
        models.City
    ).filter(models.City.id == city_id).first()


def get_city_by_name(db: Session, name: str) -> models.City:

    return db.query(
        models.City
    ).filter(models.City.name == name).first()


def create_city(
        db: Session, city: schemas.CityCreate
) -> models.City:

    db_city = models.City(
        name=city.name,
        additional_info=city.additional_info
    )

    db.add(db_city)
    db.commit()
    db.refresh(db_city)

    return db_city


def delete_city(
        db: Session, city_id: int
) -> models.City:

    city = db.query(models.City).filter(models.City.id == city_id).first()

    db.delete(city)
    db.commit()

    return city


def update_city(
        db: Session,
        current_city_id: int,
        new_city_name: str | None = None,
        new_additional_info: str | None = None,
) -> models.City:

    current_city = db.query(
        models.City
    ).filter(models.City.id == current_city_id).first()

    if new_city_name is not None:
        current_city.name = new_city_name

    if new_additional_info is not None:
        current_city.additional_info = new_additional_info

    db.commit()
    db.refresh(current_city)

    return current_city
