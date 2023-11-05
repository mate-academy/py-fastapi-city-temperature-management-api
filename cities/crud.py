from sqlalchemy.orm import Session


from cities.models import DBCity
from cities.schemas import CityCreate


def create_city(db: Session, city: CityCreate) -> DBCity:
    db_city = DBCity(**city.dict())
    db.add(db_city)
    db.commit()
    db.refresh(db_city)

    return db_city


def get_city_by_name(db: Session, name: str) -> DBCity:
    return (db.query(DBCity).filter(
        DBCity.name == name
    ).first())


def get_all_cities(db: Session) -> list[DBCity]:
    return db.query(DBCity).all()


def retrieve_city(city_id: int, db: Session) -> DBCity:
    return (db.query(DBCity).filter(
        DBCity.id == city_id
    ).first())
