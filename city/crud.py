from typing import List

from sqlalchemy.orm import Session

from . import models, schemas


def get_all_cities(db: Session) -> List[models.City]:
    return db.query(models.City).all()


def get_city(db: Session, city_id: int) -> models.City | None:
    return db.query(models.City).filter(models.City.id == city_id).first()


def get_city_by_name(db: Session, name: str) -> models.City | None:
    return (
        db.query(models.City).filter(models.City.name == name).first()
    )


def create_city(db: Session, city: schemas.CityCreate) -> models.City:
    db_city = models.City(
        name=city.name,
        additional_info=city.additional_info,
    )
    db.add(db_city)
    db.commit()
    db.refresh(db_city)

    return db_city


def update_city(
        db: Session,
        city_id: int,
        city_data: schemas.CityUpdate
) -> models.City:
    db_city = db.query(models.City).filter(models.City.id == city_id).first()
    if db_city:
        for key, value in city_data.model_dump().items():
            setattr(db_city, key, value)
        db.commit()
        db.refresh(db_city)
    return db_city


def delete_city(db: Session, city_id: int) -> bool:
    db_city = db.query(models.City).filter(models.City.id == city_id).first()
    if db_city:
        db.delete(db_city)
        db.commit()
        return True
    return False
