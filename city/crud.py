from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from city import schemas, models


def create_city(db: Session, city: schemas.CityCreate) -> models.City:
    db_city = models.City(name=city.name, additional_info=city.additional_info)
    db.add(db_city)
    db.commit()
    db.refresh(db_city)

    return db_city


def get_city_list(db: Session) -> list[models.City]:
    return db.scalars(select(models.City)).all()


def get_city(db: Session, city_id: int) -> models.City:
    db_city = db.get(models.City, city_id)

    if db_city is None:
        raise HTTPException(
            status_code=404,
            detail="City not found",
        )

    return db_city


def update_city(
    db: Session, city_id: int, city_data: schemas.CityCreate
) -> models.City:
    city = db.get(models.City, city_id)

    if city is None:
        raise HTTPException(
            status_code=404,
            detail="City not found",
        )

    update_data = city_data.model_dump()

    for field, value in update_data.items():
        setattr(city, field, value)

    db.commit()
    db.refresh(city)

    return city


def delete_city(db: Session, city_id: int) -> dict[str, str]:
    db_city = db.get(models.City, city_id)

    if db_city is None:
        raise HTTPException(
            status_code=404,
            detail="City not found",
        )

    db.delete(db_city)
    db.commit()

    return {"message": "City deleted successfully"}
