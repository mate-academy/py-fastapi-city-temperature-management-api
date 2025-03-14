from sqlalchemy.orm import Session
from .models import City, Temperature

def get_cities(db: Session):
    return db.query(City).all()

def create_city(db: Session, name: str, additional_info: str):
    city = City(name=name, additional_info=additional_info)
    db.add(city)
    db.commit()
    db.refresh(city)
    return city

def delete_city(db: Session, city_id: int):
    city = db.query(City).filter(City.id == city_id).first()
    if city:
        db.delete(city)
        db.commit()
    return city