from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.city import City
from app.schemas.city import CityCreate, CityUpdate


def get_city(db: Session, city_id: int) -> City | None:
    return db.get(City, city_id)


def get_city_by_name(db: Session, name: str) -> City | None:
    statement = select(City).where(City.name == name)
    return db.scalar(statement)


def get_cities(db: Session) -> list[City]:
    statement = select(City).order_by(City.id)
    return list(db.scalars(statement).all())


def create_city(db: Session, city_data: CityCreate) -> City:
    city = City(**city_data.model_dump())
    db.add(city)
    db.commit()
    db.refresh(city)
    return city


def update_city(db: Session, city: City, city_data: CityUpdate) -> City:
    update_values = city_data.model_dump(exclude_unset=True)
    for field, value in update_values.items():
        setattr(city, field, value)

    db.commit()
    db.refresh(city)
    return city


def delete_city(db: Session, city: City) -> None:
    db.delete(city)
    db.commit()
