from sqlalchemy.orm import Session

from cities import schemas
from cities import models


def get_city(db: Session, city_id: int) -> models.City:
    return db.query(models.City).filter(
        models.City.id == city_id
    ).first()


def get_cities(
        db: Session,
        skip: int = 0,
        limit: int = 100
) -> list[models.City]:
    return db.query(models.City).offset(skip).limit(limit).all()


def create_city(
        db: Session,
        city: schemas.CityCreate
) -> models.City:
    db_city = models.City(name=city.name, additional_info=city.additional_info)
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def update_city(
        city_id: int,
        city: schemas.CityBase,
        db: Session
) -> models.City | None:
    db_city = get_city(db, city_id)
    if not db_city:
        return None

    for key, value in city.model_dump().items():
        setattr(db_city, key, value)

    db.commit()
    db.refresh(db_city)
    return db_city


def delete_city(
        db: Session,
        city_id: int
) -> bool | None:
    db_city = get_city(db, city_id)
    if not db_city:
        return None

    db.delete(db_city)
    db.commit()
    return True
