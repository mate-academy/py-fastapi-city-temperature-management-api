from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

import schemas
from db import models


def get_all_cities(db: Session) -> List[models.City]:
    return list(db.scalars(select(models.City)).all())


def create_city(db: Session, city_data: schemas.CityCreate) -> models.City:
    db_city = models.City(**city_data.model_dump())
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def get_city_by_id(db: Session, city_id: int) -> models.City | None:
    return db.get(models.City, city_id)  # type: ignore[return-value]


def delete_city(db: Session, city_id: int) -> bool:
    city = db.get(models.City, city_id)
    if city is None:
        return False
    db.delete(city)
    db.commit()
    return True


def get_city_by_name(db: Session, city_name: str) -> models.City | None:
    return db.scalar(select(models.City).where(models.City.name == city_name))
