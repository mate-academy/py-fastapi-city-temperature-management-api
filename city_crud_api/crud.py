from typing import Optional, List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from models import DBCity, DBTemperature
from city_crud_api.schemas import CityCreate


def get_all_cities(db: Session) -> List[DBCity]:
    return db.query(DBCity).all()


def get_city(db: Session, city_id: int) -> Optional[DBCity]:
    return db.query(DBCity).filter(DBCity.id == city_id).first()


def create_city(db: Session, city: CityCreate) -> DBCity:
    db_create_city = DBCity(
        name=city.name,
        additional_info=city.additional_info,
    )
    db.add(db_create_city)
    db.commit()
    db.refresh(db_create_city)

    return db_create_city


def update_city(db: Session, city_id: int, city: CityCreate) -> DBCity:
    db_city = db.query(DBCity).filter(DBCity.id == city_id).first()
    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")
    for table_field, city_name in city.model_dump().items():
        setattr(db_city, table_field, city_name)
    db.commit()
    db.refresh(db_city)
    return db_city


def delete_city(db: Session, city_id: int) -> DBCity:
    db_city = db.query(DBCity).filter(DBCity.id == city_id).first()
    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")
    db.delete(db_city)
    db.commit()
    db.refresh(db_city)

    return db_city


def get_temperatures_by_city(
    db: Session,
    city_id: int,
) -> List[DBTemperature]:
    return db.query(DBTemperature).filter(DBTemperature.city_id == city_id).all()
