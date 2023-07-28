from typing import Optional, List
from fastapi import HTTPException
from sqlalchemy.orm import Session

from city_api.models import City
from city_api.schemas import CityCreate
from city_api.models import City as CityModel
from temperature_api.models import Temperature as TemperatureModel


def create_city(db: Session, city: CityCreate) -> City:
    db_city = CityModel(name=city.name, additional_info=city.additional_info)
    db.add(db_city)
    commit_and_refresh(db, db_city)
    return db_city


def get_cities(db: Session, skip: int = 0, limit: int = 10) -> List[City]:
    return db.query(CityModel).offset(skip).limit(limit).all()


def get_city(db: Session, city_id: int) -> Optional[City]:
    return db.query(CityModel).filter(CityModel.id == city_id).first()


def update_city(db: Session, city_id: int, city: CityCreate) -> City:
    db_city = db.query(CityModel).filter(CityModel.id == city_id).first()
    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")
    for table_field, city_name in city.model_dump().items():
        setattr(db_city, table_field, city_name)
    commit_and_refresh(db, db_city)
    return db_city


def delete_city(db: Session, city_id: int) -> City:
    db_city = db.query(CityModel).filter(CityModel.id == city_id).first()
    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")
    db.delete(db_city)
    commit_and_refresh(db, db_city)
    return db_city


def get_temperatures_by_city(
    db: Session,
    city_id: int,
    skip: int = 0,
    limit: int = 10,
):
    return db.query(TemperatureModel).filter(
        TemperatureModel.city_id == city_id
    ).offset(skip).limit(limit).all()


def commit_and_refresh(db: Session, db_obj: object):
    db.commit()
    db.refresh(db_obj)
