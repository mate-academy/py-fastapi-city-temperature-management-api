from sqlalchemy import select
from sqlalchemy.orm import Session

from models.city import City
from schemas.city import CityCreate

def get_cities(db: Session) -> list[City]:
    return list(db.scalars(select(City)).all())

def get_city(db: Session, city_id: int) -> City | None:
    return db.get(City, city_id)

def create_city(db: Session, city: CityCreate) -> City:
    existing = db.query(City).filter(City.name == city.name).first()
    if existing:
        raise ValueError("City already exists")

    db_city = City(**city.model_dump())
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city

def delete_city(db: Session, city: City) -> None:
    db.delete(city)
    db.commit()
