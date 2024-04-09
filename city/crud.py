from sqlalchemy.orm import Session
from city import models, schemas


def get_all_city(db: Session):
    return db.query(models.DBCity).all()


def create_city(db: Session, city: schemas.CityCreate):
    db_city = models.DBCity(
        name=city.name,
        additional_info=city.additional_info
    )
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def get_city(db: Session, city_id: int):
    return db.query(models.DBCity).filter(models.DBCity.id == city_id).first()


def update_city(db: Session, city_id: int, city: schemas.CityBase):
    current_city = db.get(models.DBCity, city_id)
    if not current_city:
        return None

    current_city.name = city.name
    current_city.additional_info = city.additional_info
    db.commit()
    db.refresh(current_city)

    return current_city


def delete_city(db: Session, city_id: int):
    current_city = db.get(models.DBCity, city_id)
    if current_city is None:
        return None

    db.delete(current_city)
    db.commit()
    return current_city
