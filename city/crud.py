from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from city.models import City
from schemas import CityCreate, CityUpdate


def create_city_crud(db: Session, city_data: CityCreate):
    db_city = db.scalar(select(City).where(City.name == city_data.name))
    if db_city is not None:
        raise HTTPException(status_code=409, detail="This city already exists")

    db_city = City(**city_data.model_dump())

    db.add(db_city)
    db.commit()

    db.refresh(db_city)

    return db_city


def get_all_cities(db: Session):
    return db.scalars(select(City)).all()


def get_city_or_404(db: Session, city_id: int):
    city = db.scalar(select(City).where(City.id == city_id))
    if city is None:
        raise HTTPException(status_code=404, detail="This city does not exist")
    return city


def update_city_by_id(db: Session, city_id: int, update_data: CityUpdate):
    city = get_city_or_404(db, city_id)

    for field, value in update_data.model_dump().items():
        setattr(city, field, value)

    db.commit()
    db.refresh(city)

    return city


def delete_city_crud(db: Session, city_id: int):
    city = get_city_or_404(db, city_id)

    db.delete(city)
    db.commit()
