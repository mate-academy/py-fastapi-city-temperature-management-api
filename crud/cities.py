from sqlalchemy import select
from sqlalchemy.orm import Session

from models.city import City
from schemas.city import CityCreate, CityUpdate

def create_city(db: Session, city_in: CityCreate) -> City:
    city = City(name=city_in.name, additional_info=city_in.additional_info)
    db.add(city)
    db.commit()
    db.refresh(city)
    return city

def list_cities(db: Session) -> list[City]:
    return list(db.scalars(select(City).order_by(City.id)).all())

def get_city(db: Session, city_id: int) -> City | None:
    return db.get(City, city_id)

def update_city(db: Session, city: City, city_in: CityUpdate) -> City:
    if city_in.name is not None:
        city.name = city_in.name
    if city_in.additional_info is not None:
        city.additional_info = city_in.additional_info
    db.commit()
    db.refresh(city)
    return city

def delete_city(db: Session, city: City) -> None:
    db.delete(city)
    db.commit()
