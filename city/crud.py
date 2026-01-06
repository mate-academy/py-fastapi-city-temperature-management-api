from typing import List, Optional

from sqlalchemy.orm import Session

from city.models import City
from city.schemas import CityCreate, CityUpdate


# Get city from db with id
def get_city(db: Session, city_id: int) -> Optional[City]:
    return db.get(City, city_id)


# Get all cities from db
def get_cities(db: Session, skip: int = 0, limit: int = 10) -> List[City]:
    return db.query(City).offset(skip).limit(limit).all()


# Create city
def create_city(db: Session, city_in: CityCreate) -> City:
    db_city = City(**city_in.model_dump())

    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def update_city(db: Session,
                city_id: int,
                city_in: CityUpdate) -> Optional[City]:
    db_city = db.get(City, city_id)
    if not db_city:
        return None

    update_data = city_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_city, key, value)

    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def delete_city(db: Session, city_id: int) -> bool:
    db_city = db.get(City, city_id)
    if not db_city:
        return False

    db.delete(db_city)
    db.commit()
    return True
