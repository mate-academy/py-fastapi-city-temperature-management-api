from sqlalchemy.orm import Session

from . import models, schemas


def get_cities(db: Session):
    return db.query(models.City).all()


def get_city_by_id(db: Session, city_id: int):
    city = db.query(models.City).filter(models.City.id == city_id).first()
    return city if city else {"message": "city with this id not found !"}


def create_city(db: Session, city: schemas.CityIn):
    city = models.City(**city.dict())
    db.add(city)
    db.commit()
    db.refresh(city)
    return city


def delete_city_by_id(db: Session, city_id: int):
    city = (db.query(models.City).filter(models.City.id == city_id).first())

    if city is not None:
        db.delete(city)
        db.commit()
        return {"message": "city deleted"}
    return {"message": "city not found"}
