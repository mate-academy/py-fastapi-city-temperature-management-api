from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

import models
import schemas


def get_all_cities(db: Session) -> list[models.City]:
    cities = db.scalars(select(models.City))

    return cities.all()


def get_city_by_id(
        db: Session,
        city_id: int
) -> models.City | None:
    return db.scalar(
        select(models.City).where(
            models.City.id == city_id)
    )


def get_city_by_name(
        db: Session,
        name: str
) -> models.City | None:
    return db.scalar(
        select(models.City).where(
            models.City.name == name)
    )


def create_one_city(
        db: Session,
        city: schemas.CityCreate
) -> models.City:
    new_city = models.City(
        name=city.name,
        additional_info=city.additional_info,
    )
    db.add(new_city)
    db.commit()
    db.refresh(new_city)

    return new_city


def delete_city(db: Session, city_id: int) -> None:
    city = db.scalar(
        select(models.City).where(models.City.id == city_id)
    )

    if city is None:
        raise HTTPException(status_code=404, detail="City not found")

    db.delete(city)
    db.commit()
