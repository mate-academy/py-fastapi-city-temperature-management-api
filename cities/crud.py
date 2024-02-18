from typing import Optional
from cities.schemas import CityBase
from dependencies import db_dependency
from cities import models
from fastapi import HTTPException


def get_all_cities(db: db_dependency) -> list[models.City]:
    return db.query(models.City).all()


def get_city_by_id(db: db_dependency, city_id: int) -> Optional[models.City]:
    return db.query(models.City).filter(models.City.id == city_id).first()


def create_city(db: db_dependency, city: CityBase) -> Optional[models.City]:
    db_city = models.City(name=city.name, additional_info=city.additional_info)

    db.add(db_city)
    db.commit()
    db.refresh(db_city)

    return db_city


def update_city_by_id(
    db: db_dependency, city: CityBase, city_id: int
) -> Optional[models.City]:
    db_city = db.query(models.City).filter(models.City.id == city_id).first()

    db_city.name = city.name
    db_city.additional_info = city.additional_info

    db.add(db_city)
    db.commit()

    return db_city


def delete_city_by_id(db: db_dependency, city_id: int) -> None:
    db.query(models.City).filter(models.City.id == city_id).delete()

    db.commit()
