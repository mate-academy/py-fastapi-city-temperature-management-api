from sqlalchemy import select
from sqlalchemy.orm import Session

from city.models import City

from city.schema import CityCreate
from city.exceptions import InvalidCityIdException


def get_all_cities(db: Session):
    return db.scalars(select(City)).all()


def create_city(db: Session, city_data: CityCreate):
    db_city = City(**city_data.model_dump())
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def get_city_by_id(db: Session, city_id: int):
    return db.scalars(select(City).where(City.id == city_id)).first()


def update_city(db: Session, city_id: int, city_data: CityCreate):
    city = db.get(City, city_id)

    if not city:
        raise InvalidCityIdException("City with this id doesn't exist")

    for field, value in city_data.model_dump().items():
        setattr(city, field, value)

    db.commit()
    db.refresh(city)
    return city


def delete_city(db: Session, city_id: int):
    city_to_delete = db.get(City, city_id)
    if not city_to_delete:
        raise InvalidCityIdException("City with this id doesn't exist")
    db.delete(city_to_delete)
    db.commit()
    return city_to_delete
