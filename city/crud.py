from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session

from city import models
from city import schemas


def get_existing_city(db: Session, city_id: int) -> Optional[models.City]:
    db_city = db.query(models.City).filter(
        models.City.id == city_id
    ).first()
    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city


def get_city_by_name(db: Session, name: str) -> None:
    db_city = db.query(models.City).filter(
        models.City.name == name
    ).first()
    if db_city:
        raise HTTPException(
            status_code=400, detail="Such name for City already exists"
        )


def create_city(db: Session, city: schemas.CityCreate) -> models.City:
    get_city_by_name(db=db, name=city.name)
    db_city = models.City(
        name=city.name,
        additional_info=city.additional_info
    )
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def get_all_cities(
        db: Session,
        skip: int = 0,
        limit: int = 10
) -> List[models.City]:
    return db.query(models.City).offset(skip).limit(limit).all()


def update_city(
        db: Session,
        city_id: int,
        city: schemas.CityUpdate
) -> models.City:
    db_city = get_existing_city(db=db, city_id=city_id)

    db_city.name = city.name
    db_city.additional_info = city.additional_info
    db.commit()
    db.refresh(db_city)
    return db_city


def delete_city(db: Session, city_id: int) -> models.City:
    db_city = get_existing_city(db=db, city_id=city_id)

    db.delete(db_city)
    db.commit()
    return db_city
