from sqlalchemy.orm import Session
from app.models.city import City
from app.schemas.city import CityCreate


def create_city(db: Session, city: CityCreate):
    db_city = City(name=city.name, additional_info=city.additional_info)
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def get_cities(db: Session):
    return db.query(City).all()


def get_city_by_id(db: Session, city_id: int):
    return db.query(City).filter(City.id == city_id).first()


def update_city(db: Session, city_id: int, city: CityCreate):
    db_city = db.query(City).filter(City.id == city_id).first()
    if db_city:
        db_city.name = city.name
        db_city.additional_info = city.additional_info
        db.commit()
        db.refresh(db_city)
    return db_city


def delete_city(db: Session, city_id: int):
    db_city = db.query(City).filter(City.id == city_id).first()
    if db_city:
        db.delete(db_city)
        db.commit()
    return db_city
