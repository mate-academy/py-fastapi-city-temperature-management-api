from sqlalchemy.orm import Session

from city import models, schemas


def get_cities(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.City).offset(skip).limit(limit).all()


def create_city(db: Session, city: schemas.CityCreate):
    db_city = models.City(**city.dict())

    db.add(db_city)
    db.commit()
    db.refresh(db_city)

    return db_city


def delete_city(db: Session, city_id: int):
    db_city = db.query(models.City).filter(models.City.id == city_id).first()

    if db_city:
        db.delete(db_city)
        db.commit()

    return db_city
