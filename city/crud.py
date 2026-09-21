from sqlalchemy import select
from sqlalchemy.orm import Session
import schemas
import models

from city.models import City


def is_city_in_db(db: Session, city_name: str):
    return db.scalar(select(City).where(City.name == city_name))


def create_new_city(db: Session, city_data: schemas.CityBase):
    city = models.City(
        name=city_data.name,
        additional_info=city_data.additional_info
    )
    db.add(city)
    db.commit()
    db.refresh(city)
    return city


def put_city(db: Session, city_data: schemas.CityBase, city_id: int):
    city = db.get(models.City, city_id)

    if city is None:
        return None

    city.name = city_data.name
    city.additional_info = city_data.additional_info

    db.commit()
    db.refresh(city)

    return city


def del_city(db: Session, city_id: int):
    city = db.get(models.City, city_id)

    if city is None:
        return None

    db.delete(city)
    db.commit()
    return city
