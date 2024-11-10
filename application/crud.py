from sqlalchemy.orm import Session
from application import models, schemas


def create_city(db: Session, city: schemas.CityCreate):
    db_city = models.City(name=city.name, additional_info=city.additional_info)
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def get_cities(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.City).offset(skip).limit(limit).all()


def get_city(db: Session, city_id: int):
    return db.query(models.City).filter(models.City.id == city_id).first()


def delete_city(db: Session, city_id: int):
    db_city = get_city(db, city_id)
    if db_city is None:
        return {"success": False, "message": f"City with ID {city_id} not found."}

    db.delete(db_city)
    db.commit()
    return {"success": True, "message": f"City with ID {city_id} has been deleted."}
