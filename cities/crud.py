from sqlalchemy.orm import Session

from models import CityDB
from schemas import CityCreate, CityUpdate


def create_city(db: Session, city: CityCreate):
    db_city = CityDB(
        name=city.name,
        additional_info=city.bio,
    )
    db.add(db_city)
    db.commit()
    db.refresh(db_city)

    return db_city


def read_all_cities(db: Session, skip: int = 0, limit: int = 10):
    return db.query(CityDB).offset(skip).limit(limit).all()


def update_city(db: Session, city_id: int, city: CityUpdate):
    db_city = db.query(CityDB).filter(CityDB.id == city_id).first()

    for key, value in city.model_dump().items():
        setattr(db_city, key, value)
    db.commit()
    db.refresh(db_city)
    return db_city


def delete_city(db: Session, city: CityDB):
    db.delete(city)
    db.commit()
    return city


def get_city_by_id(db: Session, city_id: int):
    return db.query(CityDB).filter(CityDB.id == city_id).first()
