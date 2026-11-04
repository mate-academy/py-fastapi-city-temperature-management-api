from fastapi import HTTPException

from sqlalchemy import select
from sqlalchemy.orm import Session

from cities.models import City
from cities.schemas import CreateCity, UpdateCity


def get_city_list(db: Session):
    return db.scalars(select(City)).all()


def get_city(db: Session, city_id: int):
    city = db.scalars(select(City).where(City.id == city_id)).first()

    if not city:
        raise HTTPException(
            status_code=404,
            detail="City not found"
        )

    return city


def create_city(db:Session, city: CreateCity):
    db_city = City(
        name=city.name,
        additional_info=city.additional_info
    )
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def update_city(db:Session, city_id: int, city: UpdateCity):
    db_city = get_city(db, city_id)
    update_data = city.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_city, key, value)
    db.commit()
    db.refresh(db_city)
    return db_city


def delete_city(db:Session, city_id: int):
    db_city = get_city(db, city_id)

    db.delete(db_city)
    db.commit()
    return "City deleted successfully"