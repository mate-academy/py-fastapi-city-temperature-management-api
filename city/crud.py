from fastapi import HTTPException
from sqlalchemy.orm import Session

from city import models
from city.schemas import CityCreate


def create_city(db: Session, city: CityCreate):
    db_city = models.City(
        name=city.name,
        additional_info=city.additional_info
    )
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def get_cities(db: Session):
    return db.query(models.City).all()


def get_city(db: Session, city_id: int):
    return db.query(models.City).get(city_id)


def update_city_by_id(db: Session, city_id: int, city: CityCreate):
    city_to_update = get_city(db, city_id)
    if not city_to_update:
        raise HTTPException(status_code=404, detail="City not found")
    city_to_update.name = city.name
    city_to_update.additional_info = city.additional_info
    db.commit()
    db.refresh(city_to_update)
    return city_to_update


def delete_city_by_id(db: Session, city_id: int):
    city_to_delete = get_city(db, city_id)
    if not city_to_delete:
        raise HTTPException(status_code=404, detail="City not found")
    db.delete(city_to_delete)
    db.commit()
    return city_to_delete
