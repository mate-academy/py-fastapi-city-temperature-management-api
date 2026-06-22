from sqlalchemy import select
from sqlalchemy.orm import Session

from app.schemas import city as city_schema
from app.models import city as city_model


def create_city(
        db: Session,
        city: city_schema.CityCreate
) -> city_model.City:
    db_city = city_model.City(**city.model_dump())
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city

def get_city(db: Session, city_id: int) -> city_model.City | None:
    return db.scalar(
        select(
            city_model.City
        ).where(
            city_model.City.id == city_id
        )
    )

def get_cities(
        db: Session
) -> list[city_model.City]:
    return list(db.scalars(select(city_model.City)))

def delete_city(
        db: Session,
        city_id: int
) -> city_model.City | None:
    db_city = get_city(db, city_id)
    if not db_city:
        return None
    db.delete(db_city)
    db.commit()
    return db_city

def update_city(
        db: Session,
        city_id: int,
        city_update: city_schema.CityCreate
) -> city_model.City | None:
    db_city = get_city(db, city_id)
    if not db_city:
        return None
    update_data = city_update.model_dump()
    for key, value in update_data.items():
        setattr(db_city, key, value)
    db.commit()
    db.refresh(db_city)
    return db_city
