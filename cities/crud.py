from fastapi import HTTPException
from sqlalchemy.orm import Session

from cities import schemas
import models


def get_cities(db: Session, skip: int = 0, limit: int = 10) -> list[models.City]:
    return db.query(models.City).offset(skip).limit(limit).all()


def create_city(db: Session, city: schemas.CityCreate):
    db_city = models.City(**city.model_dump())
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def delete_city(db: Session, city_id: int):
    db_city = db.query(models.City).filter(models.City.id == city_id).first()

    if db_city is None:
        raise HTTPException(status_code=400, detail={"error": f"No such city with {city_id} id"})

    db.delete(db_city)
    db.commit()
    return f"City with {city_id} id was deleted"
