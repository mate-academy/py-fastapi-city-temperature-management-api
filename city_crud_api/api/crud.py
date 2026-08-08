from sqlalchemy import select
from sqlalchemy.orm import Session

from city_crud_api.api.schemas import CityCreate
from city_crud_api.db import models


def get_all_cities(db: Session):
    statement = select(models.City)
    return list(db.scalars(statement).all())


def create_new_city(city_data: CityCreate, db: Session):
    db_city = models.City(
        name=city_data.name,
        additional_info=city_data.additional_info,
    )

    db.add(db_city)
    db.commit()
    db.refresh(db_city)

    return db_city


def retrieve_specific_city(db: Session, city_id: int):
    return db.get(models.City, city_id)


def update_specific_city(
    db: Session,
    city_id: int,
    city_data: CityCreate,
):
    db_city = db.get(models.City, city_id)

    if db_city is None:
        return None

    db_city.name = city_data.name
    db_city.additional_info = city_data.additional_info

    db.commit()
    db.refresh(db_city)

    return db_city


def delete_specific_city(db: Session, city_id: int):
    db_city = db.get(models.City, city_id)

    if db_city is None:
        return False

    db.delete(db_city)
    db.commit()

    return True
