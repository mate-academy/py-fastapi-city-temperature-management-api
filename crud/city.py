from sqlalchemy import Sequence, select
from sqlalchemy.orm import Session

from models import City
from schemas.city import CityCreate, CityUpdate


def create_city(db: Session, city: CityCreate) -> City:
    db_city = City(**city.model_dump())

    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city

def get_cities(db: Session, skip: int = 0, limit: int = 100) -> Sequence[City]:
    return db.scalars(select(City).offset(skip).limit(limit)).all()


def get_city(db: Session, city_id: int) -> City | None:
    return db.scalars(select(City).where(City.id == city_id)).first()


def get_city_by_name(db: Session, name: str) -> City | None:
    return db.query(City).filter(City.name == name).first()


def update_city(db: Session, city_id: int, city: CityUpdate) -> City | None:
    db_city = get_city(db, city_id)

    if not db_city:
        return None

    update_data = city.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(db_city, field, value)

    db.commit()
    db.refresh(db_city)

    return db_city


def delete_city(db: Session, city_id: int) -> bool:
    db_city = get_city(db, city_id)

    if not db_city:
        return False

    db.delete(db_city)
    db.commit()

    return True
