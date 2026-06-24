from sqlalchemy.orm import Session
from sqlalchemy import select
from city.models import City
from city.schemas import CityCreate


def create_city(db: Session, city: CityCreate) -> City:
    db_city = City(**city.model_dump())
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def get_cities(db: Session) -> list[City]:
    return list(db.execute(select(City)).scalars().all())


def delete_city(db: Session, city_id: int) -> City | None:
    db_city = db.execute(select(City).where(City.id == city_id)).scalar_one_or_none()
    if db_city:
        db.delete(db_city)
        db.commit()
    return db_city
