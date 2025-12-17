import datetime
from sqlalchemy.orm import Session
from db.models import DBCity, DBTemperature
from schemas import CityCreate


def create_city(
    db: Session,
    city_data: CityCreate,
):
    city = DBCity(**city_data.dict())
    db.add(city)
    db.commit()
    db.refresh(city)
    return city


def get_cities(db: Session):
    return db.query(DBCity).all()


def get_city(
    db: Session,
    city_id: int,
):
    return db.query(DBCity).filter(DBCity.id == city_id).first()


def delete_city(
    db: Session,
    city_id: int,
):
    city = get_city(db, city_id)
    if city:
        db.delete(city)
        db.commit()
    return city


def get_temperatures(
    db: Session,
    city_id: int | None = None,
):
    query = db.query(DBTemperature)
    if city_id:
        query = query.filter(DBTemperature.city_id == city_id)
    return query.all()


def create_temperature(
    db: Session,
    city_id: int,
    temperature: float,
):
    temp = DBTemperature(
        city_id=city_id,
        temperature=temperature,
        date_time=datetime.datetime.utcnow(),
    )
    db.add(temp)
    db.commit()
    db.refresh(temp)
    return temp
