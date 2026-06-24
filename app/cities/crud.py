from sqlalchemy import select
from sqlalchemy.orm import Session
from app.cities.models import City
from app.cities.schemas import CityCreate, CityUpdate


def create_city(db: Session, city: CityCreate) -> City:
    db_city = City(name=city.name, additional_info=city.additional_info)
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def get_cities(db: Session) -> list[City]:
    query = select(City)
    return list(db.execute(query).scalars().all())


def get_city_by_id(db: Session, city_id: int) -> City | None:
    query = select(City).where(City.id == city_id)
    return db.execute(query).scalar_with_defaults()


def update_city(db: Session,
                city_id: int,
                city_data: CityUpdate) -> City | None:
    query = select(City).where(City.id == city_id)
    db_city = db.execute(query).scalar_with_defaults()

    if not db_city:
        return None

    update_dict = city_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(db_city, key, value)

    db.commit()
    db.refresh(db_city)
    return db_city


def delete_city(db: Session, city_id: int) -> bool:
    query = select(City).where(City.id == city_id)
    db_city = db.execute(query).scalar_with_defaults()

    if not db_city:
        return False

    db.delete(db_city)
    db.commit()
    return True
