from sqlalchemy.orm import Session
from city import schemas
from city.models import City


def get_cities_list(db: Session, skip: int = 0, limit: int = 100):
    return db.query(City).offset(skip).limit(limit).all()


def create_city(db: Session, city: schemas.CityCreate) -> City:
    db_city = City(**city.model_dump())
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def delete_city(db: Session, city_id: int) -> bool:
    db_city = db.get(City, int(city_id))
    if db_city:
        db.delete(db_city)
        db.commit()
        return True
