from datetime import datetime
from http.client import HTTPException

from sqlalchemy.orm import Session

from models import City, Temperature
from schemas import CityCreate, TemperatureCreate


async def create_city(db: Session, city: CityCreate):
    db_city = City(name=city.name, additional_info=city.additional_info)
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return await db_city


async def get_city(db: Session, city_id: int):
    return await db.query(City).filter(City.id == city_id).first()


async def get_cities(db: Session, skip: int = 0, limit: int = 10):
    return await db.query(City).offset(skip).limit(limit).all()


async def update_city(db: Session, city_id: int, city: CityCreate):
    try:
        db_city = db.query(City).filter(City.id == city_id).first()
        if db_city:
            db_city.name = city.name
            db_city.additional_info = city.additional_info
            db.commit()
            db.refresh(db_city)
        return await db_city
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


async def delete_city(db: Session, city_id: int):
    db_city = db.query(City).filter(City.id == city_id).first()
    if db_city:
        db.delete(db_city)
        db.commit()
    return await db_city


async def create_temperature(db: Session, temperature: TemperatureCreate):
    db_temperature = Temperature(
        city_id=temperature.city_id,
        date_time=datetime.utcnow(),
        temperature=temperature.temperature
    )
    db.add(db_temperature)
    db.commit()
    db.refresh(db_temperature)
    return await db_temperature


async def get_temperatures(db: Session, skip: int = 0, limit: int = 10):
    return await db.query(Temperature).offset(skip).limit(limit).all()


async def get_temperatures_by_city(db: Session, city_id: int, skip: int = 0, limit: int = 10):
    return await db.query(Temperature).filter(Temperature.city_id == city_id).offset(skip).limit(limit).all()
