from datetime import datetime

from sqlalchemy.orm import Session


from models import City, Temperature
from schemas import CityCreate
from services.weather import get_temp


def get_city_by_name(db: Session, name: str):
    return (
        db.query(City).filter(City.name == name).first()
    )

def get_all_cities(
        db: Session,
        skip: int = 0,
        limit: int = 100
):
    return (
        db.query(City)
        .offset(skip)
        .limit(limit)
        .all())

def create_city(db: Session, city: CityCreate):
    db_city = City(
        name=city.name,
        additional_info=city.additional_info,
    )
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city

def get_city_by_id(db: Session, city_id: int):
    return db.query(City).filter(City.id == city_id).first()

def update_city(db: Session, city_id: int, city: CityCreate):
    db_city = get_city_by_id(db, city_id)

    db_city.name = city.name
    db_city.additional_info = city.additional_info

    db.commit()
    db.refresh(db_city)

    return db_city

def delete_city(db: Session, city_id: int):
    city = get_city_by_id(db, city_id)
    db.delete(city)
    db.commit()

async def temperature_update(db: Session):
    cities = db.query(City).all()

    for city in cities:
        temp = await get_temp(city.name)

        db.add(
            Temperature(
                city_id=city.id,
                date_time=datetime.utcnow(),
                temperature=temp
            )
        )

    db.commit()

def get_all_temperature(
        db: Session,
        city_id: int | None = None,
        skip: int = 0,
        limit: int = 100
):
    query = db.query(Temperature)

    if city_id is not None:
        query = query.filter(
            Temperature.city_id == city_id
        )

    return query.offset(skip).limit(limit).all()