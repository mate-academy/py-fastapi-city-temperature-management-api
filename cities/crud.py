from sqlalchemy.orm import Session
from sqlalchemy import select

from cities import schemas
from cities import models


def create_city(db: Session, city: schemas.CityCreate):
    db_city = models.City(
        name=city.name,
        additional_info=city.additional_info,
    )
    db.add(db_city)
    db.commit()
    db.refresh(db_city)

    return db_city


def get_all_cities(db: Session):
    return db.scalars(select(models.City)).all()


def get_city(db: Session, city_id: int):
    return db.scalars(select(models.City).where(models.City.id == city_id)).first()


def get_city_by_name(db: Session, name: str):
    return db.scalar(select(models.City).where(models.City.name == name))


def update_city(db: Session, city_id: int, city_data: schemas.CityCreate):
    db_city = get_city(db, city_id)

    if not db_city:
        return None

    db_city.name = city_data.name
    db_city.additional_info = city_data.additional_info

    db.commit()
    db.refresh(db_city)

    return db_city


def delete_city(db: Session, city_id: int) -> bool:
    db_city = get_city(db, city_id)

    if not db_city:
        return False

    db.delete(db_city)
    db.commit()

    return True
