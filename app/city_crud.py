from sqlalchemy.orm import Session
from app.models import City


def get_cities(db: Session):
    return db.query(City).all()


def create_city(db: Session, city: City):
    db.add(city)
    db.commit()
    db.refresh(city)
    return city


def delete_city(db: Session, city_id: int):
    city = db.query(City).filter(City.id == city_id).first()
    if city:
        db.delete(city)
        db.commit()
