from typing import List, Optional

from sqlalchemy.orm import Session
from fastapi import HTTPException
from city import models, schemas


def get_all_city(db: Session) -> List[models.City]:
    return db.query(models.City).all()


def get_city_by_name_and_info(
    db: Session, name: str, additional_info: str
) -> List[models.City]:
    return (
        db.query(models.City)
        .filter(
            models.City.name == name,
            models.City.additional_info == additional_info,
        )
        .first()
    )


def create_city(db: Session, city: schemas.CityCreate) -> models.City:
    db_city = get_city_by_name_and_info(db, city.name, city.additional_info)
    if db_city:
        raise HTTPException(
            status_code=400,
            detail="Such name and additional info for city already exists",
        )
    city = models.City(name=city.name, additional_info=city.additional_info)
    db.add(city)
    db.commit()
    db.refresh(city)

    return city


def get_city_by_id(db: Session, city_id: int) -> Optional[models.City]:
    return (db.query(models.City).filter(models.City.id == city_id)).first()


def delete_city_by_id(db: Session, city_id: int) -> models.City:
    db_city = get_city_by_id(db, city_id)
    if db_city is None:
        return HTTPException(status_code=404, detail="City not found")
    db.delete(db_city)
    db.commit()
    return db_city
