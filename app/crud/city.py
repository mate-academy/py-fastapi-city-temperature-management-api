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

def delete_city(db: Session, city_id: int):
    db_city = db.query(City).get(city_id)
    if db_city:
        db.delete(db_city)
        db.commit()
    return db_city
