from sqlalchemy.orm import Session

from app.models.city import City
from app.schemas.city import CityCreate


def create_city(db: Session, city: CityCreate) -> City:
    db_city = City(
        name=city.name,
        additional_info=city.additional_info,
    )
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def get_cities(db: Session) -> list[City]:
    return db.query(City).all()


def get_city(db: Session, city_id: int) -> City | None:
    return db.query(City).filter(City.id == city_id).first()


def update_city(
    db: Session,
    city_id: int,
    city: CityCreate,
) -> City | None:
    db_city = get_city(db, city_id)
    if not db_city:
        return None

    db_city.name = city.name
    db_city.additional_info = city.additional_info

    db.commit()
    db.refresh(db_city)
    return db_city


def delete_city(db: Session, city_id: int) -> bool:
    db_city = get_city(db, city_id)
    if not db_city:
        return False

    db.delete(db_city)
    db.commit()
    return True
