from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import City
from app.schemas.city import CityCreate


def get_cities(database: Session):
    return database.scalars(
        select(City)
    ).all()


def get_city_by_id(
        database: Session,
        city_id: int
):
    return database.scalar(
        select(City).where(City.id == city_id)
    )


def create_city(
        database: Session,
        city: CityCreate
):
    database_city = City(
        name=city.name,
        additional_info=city.additional_info
    )

    database.add(database_city)
    database.commit()
    database.refresh(database_city)

    return database_city


def delete_city(
        database: Session,
        city: City
):
    database.delete(city)
    database.commit()
