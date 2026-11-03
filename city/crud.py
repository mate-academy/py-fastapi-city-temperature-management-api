from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from city import models, schemas


def get_all_cities(db: Session) -> Sequence[models.DBCity]:
    return db.scalars(select(models.DBCity)).all()


def get_city_by_id(db: Session, city_id: int) -> models.DBCity | None:
    return db.get(models.DBCity, city_id)


def get_city_by_name(db: Session, name: str) -> models.DBCity | None:
    return db.scalars(
        select(models.DBCity).where(models.DBCity.name == name)
    ).first()


def create_city(db: Session, city: schemas.CityCreate) -> models.DBCity:
    db_city = models.DBCity(
        name=city.name,
        additional_info=city.additional_info,
    )

    db.add(db_city)
    db.commit()
    db.refresh(db_city)

    return db_city


def update_city(
    db: Session, db_city: models.DBCity, city: schemas.CityUpdate
) -> models.DBCity:
    db_city.name = city.name
    db_city.additional_info = city.additional_info

    db.commit()
    db.refresh(db_city)

    return db_city


def delete_city(db: Session, db_city: models.DBCity) -> models.DBCity:
    db.delete(db_city)
    db.commit()

    return db_city
