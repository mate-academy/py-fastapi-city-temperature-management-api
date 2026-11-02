from sqlalchemy import select
from sqlalchemy.orm import Session

from src.city.models import City
from src.city.schemas import CityCreate, CityUpdate


def get_cities(db: Session, skip: int = 0, limit: int | None = 100) -> list[City]:
    stmt = select(City).order_by(City.id).offset(skip).limit(limit)
    return list(db.scalars(stmt).all())


def get_city(db: Session, city_id: int) -> City | None:
    return db.get(City, city_id)


def get_city_by_name(db: Session, name: str) -> City | None:
    return db.scalar(select(City).where(City.name == name))


def create_city(db: Session, city: CityCreate) -> City:
    db_city = City(**city.model_dump())
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def update_city(db: Session, db_city: City, city: CityUpdate) -> City:
    for key, value in city.model_dump(exclude_unset=True).items():
        setattr(db_city, key, value)
    db.commit()
    db.refresh(db_city)
    return db_city


def delete_city(db: Session, db_city: City) -> None:
    db.delete(db_city)
    db.commit()
