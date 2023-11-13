from fastapi import HTTPException
from sqlalchemy.orm import Session

from city import models
from city.models import City
from city.schemas import CityCreate


def get_all_cities(db: Session):
    return db.query(City).all()


def create_city(database: Session, city: CityCreate):
    db_city = models.City(name=city.name, additional_info=city.additional_info)
    database.add(db_city)
    database.commit()
    database.refresh(db_city)

    return db_city


def get_city(database: Session, city_id: int):
    city = database.query(City).filter(City.id == city_id).first()
    if city is None:
        raise HTTPException(status_code=404, detail="city not found")
    return city


def get_city_by_name(database: Session, city_name: int):
    city = database.query(City).filter(City.name == city_name).first()
    if city is None:
        raise HTTPException(status_code=404, detail="city not found")
    return city


def delete_city(database: Session, city_id: int):
    db_city = get_city(database, city_id)
    if db_city:
        database.delete(db_city)
        database.commit()
