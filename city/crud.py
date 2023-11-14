from sqlalchemy.orm import Session

from city import schemas
from city.schemas import CityCreate
from city.models import DBCity


def get_all_cities(db: Session):
    return db.query(DBCity).all()


def create_cities(db: Session, city: CityCreate):
    db_city = DBCity(name=city.name, additional_info=city.additional_info)
    db.add(db_city)
    db.commit()
    db.refresh(db_city)

    return db_city


def get_city(db: Session, city_id: int):
    return db.query(DBCity).filter(DBCity.id == city_id).first()


def update_city(db: Session, city: DBCity, city_update: schemas.City):
    for attr, value in city_update.dict().items():
        setattr(city, attr, value)
    db.commit()
    db.refresh(city)
    return city


def delete_city(db: Session, city_id: int):
    city = db.query(DBCity).filter(DBCity.id == city_id).first()
    if city:
        db.delete(city)
        db.commit()
        return True
    return False
