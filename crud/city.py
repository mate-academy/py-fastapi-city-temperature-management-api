from sqlalchemy import select
from sqlalchemy.orm import Session

from models.city import City
from schemas.city import CityCreate

def get_cities(db: Session) -> list[City]:
    return list(db.scalars(select(City)).all())

def get_city(db: Session, city_id: int) -> City | None:
    return db.get(City, city_id)

def create_city(db: Session, city_data: CityCreate) -> City:
    city = City(**city_data.model_dump())
    db.add(city)
    db.commit()
    db.refresh(city)
    return city

def delete_city(db: Session, city_id: int) -> None:
    city = get_city(db, city_id)
    if city:
        db.delete(city)
        db.commit()
