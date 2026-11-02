from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models import City, Temperature
from app.schemas import CityCreate, CityUpdate


def get_city(session: Session, city_id: int) -> City | None:
    return session.get(City, city_id)


def get_cities(session: Session, skip: int = 0, limit: int = 100) -> list[City]:
    return list(session.scalars(select(City).offset(skip).limit(limit)).all())


def create_city(session: Session, city_in: CityCreate) -> City:
    db_city = City(**city_in.model_dump())
    session.add(db_city)
    session.commit()
    session.refresh(db_city)
    return db_city


def update_city(session: Session, db_city: City, city_in: CityUpdate) -> City:
    update_data = city_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_city, key, value)
    session.commit()
    session.refresh(db_city)
    return db_city


def delete_city(session: Session, db_city: City) -> City:
    session.delete(db_city)
    session.commit()
    return db_city


def get_temperatures(session: Session, city_id: int | None = None) -> list[Temperature]:
    stmt = select(Temperature)
    if city_id is not None:
        stmt = stmt.where(Temperature.city_id == city_id)
    return list(session.scalars(stmt).all())
