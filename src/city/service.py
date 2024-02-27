from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.city import models
from src.city import schemas


def get_all_cities(db: Session):
    return db.query(models.City).all()


def create_city(db: Session, city: schemas.CityCreate):
    db_city = models.City(
        name=city.name,
        additional_info=city.additional_info
    )

    db.add(db_city)
    db.commit()
    db.refresh(db_city)

    return db_city


def get_city(db: Session, city_id: int):
    return db.query(models.City).filter(models.City.id == city_id).first()


def update_city(db: Session, city_id: int, city: schemas.CityCreate):
    db_city = get_city(db=db, city_id=city_id)

    if db_city is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"There is not city with id: {city_id}"
        )

    db_city.name = city.name
    db_city.additional_info = city.additional_info

    db.commit()

    return db_city


def delete_city(db: Session, city_id: int):
    db_city = get_city(db=db, city_id=city_id)

    db.delete(db_city)
    db.commit()

    return {"message": "City deleted successfully"}
