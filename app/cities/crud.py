from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List, Optional
from app.cities import models, schemas


def get_city(db: Session, city_id: int) -> Optional[models.City]:
    return db.get(models.City, city_id)


def get_city_by_name(db: Session, name: str) -> Optional[models.City]:
    return db.scalar(select(models.City).where(models.City.name == name))


def get_cities(db: Session) -> List[models.City]:
    return list(db.scalars(select(models.City)).all())


def create_city(db: Session, city: schemas.CityCreate) -> models.City:
    db_city = models.City(name=city.name, additional_info=city.additional_info)
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def update_city(
    db: Session, db_city: models.City, city_update: schemas.CityUpdate
) -> models.City:
    db_city.name = city_update.name
    db_city.additional_info = city_update.additional_info
    db.commit()
    db.refresh(db_city)
    return db_city


def delete_city(db: Session, db_city: models.City) -> None:
    db.delete(db_city)
    db.commit()
