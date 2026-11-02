from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from cities import models
from cities.schemas import CreateCitySchema


def create_city(db_session: Session, city: CreateCitySchema) -> models.City:
    db_city = models.City(**city.model_dump())
    db_session.add(db_city)
    db_session.commit()
    db_session.refresh(db_city)
    return db_city

def get_cities(db_session: Session) -> list[models.City]:
    return list(db_session.scalars(select(models.City)).all())

def get_city_by_id(db_session: Session, city_id: int) -> models.City | None:
    return db_session.scalar(select(models.City).where(models.City.id == city_id))


def delete_city(db_session: Session, city_id: int) -> bool:
    db_user = db_session.get(models.City, city_id)
    if db_user is None:
        return False

    db_session.delete(db_user)
    db_session.commit()
    return True