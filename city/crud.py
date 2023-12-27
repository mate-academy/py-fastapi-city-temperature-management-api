from sqlalchemy.orm import Session

from city import models, schemas
from city.models import City


def get_all_cities(
        db: Session,
        skip: int = 0,
        limit: int = 10
) -> list[City]:
    return db.query(models.City).offset(skip).limit(limit).all()


def get_single_city(
        db: Session,
        city_id: int
) -> City | None:
    return db.query(models.City).filter(
        models.City.id == city_id
    ).first()


def get_city_name(db: Session, name: str) -> City | None:
    return (
        db.query(models.City).filter(models.City.name == name).first()
    )


def create_city(db: Session, city: schemas.CityCreate) -> City:
    db_city = models.City(
        name=city.name,
        additional_info=city.additional_info
    )
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def update_city(
        db: Session,
        city_id: int,
        name: str,
        additional_info: str
) -> City:
    db_city = db.query(models.City).filter(models.City.id == city_id).first()

    if db_city:
        db_city.name = name
        db_city.additional_info = additional_info
        db.commit()
        db.refresh(db_city)
        return db_city


def delete_city(db: Session, city_id: int) -> dict:
    db_city = db.query(models.City).filter(models.City.id == city_id).first()

    if db_city:
        db.delete(db_city)
        db.commit()
        return db_city
