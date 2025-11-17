from typing import Any
from sqlalchemy.orm import Session

from app.models.city import DBCity
from app.schemas.city import CityCreate, CityUpdate


def create_city(db: Session, city: CityCreate) -> Any:
    db_city = DBCity(
        name=city.name,
        additional_info=city.additional_info
    )
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def get_cities(
        db: Session,
        skip: int = 0,
        limit: int = 10
) -> Any:
    return (
        db.query(DBCity)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_city(db: Session, city_id: int) -> Any:
    return (
        db.query(
            DBCity
        ).filter(
            DBCity.id == city_id
        ).first()
    )


def update_city(
        db: Session,
        city_id: int,
        update: CityUpdate
) -> Any:
    city = get_city(db, city_id)
    if not city:
        return None

    if update.additional_info is not None:
        city.additional_info = update.additional_info

    db.commit()
    db.refresh(city)
    return city


def delete_city(db: Session, city_id: int) -> Any:
    city = get_city(db, city_id)
    if not city:
        return False

    db.delete(city)
    db.commit()
    return True
