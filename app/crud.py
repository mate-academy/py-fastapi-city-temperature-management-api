from sqlalchemy.orm import Session
from models import City, Temperature
from schemas import CityCreate, CityUpdate
from datetime import datetime


def create_city(db: Session, city: CityCreate) -> City:
    db_city = City(
        name=city.name,
        additional_info=city.additional_info
    )
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def get_cities(db: Session):
    return db.query(City).all()


def get_city(db: Session, city_id: int) -> City | None:
    return db.query(City).filter(City.id == city_id).first()


def update_city(db: Session, city_id: int, city_update: CityUpdate) -> City | None:
    city = get_city(db, city_id)
    if not city:
        return None

    city.name = city_update.name
    city.additional_info = city_update.additional_info
    db.commit()
    db.refresh(city)
    return city


def delete_city(db: Session, city_id: int) -> bool:
    city = get_city(db, city_id)
    if not city:
        return False

    db.delete(city)
    db.commit()
    return True


def create_temperature(
    db: Session,
    city_id: int,
    temperature: float
) -> Temperature:
    temp = Temperature(
        city_id=city_id,
        temperature=temperature,
        date_time=datetime.utcnow()
    )
    db.add(temp)
    db.commit()
    db.refresh(temp)
    return temp


def get_temperatures(
    db: Session,
    city_id: int | None = None
):
    query = db.query(Temperature)
    if city_id is not None:
        query = query.filter(Temperature.city_id == city_id)
    return query.all()
