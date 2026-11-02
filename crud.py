from dns import name
from sqlalchemy.orm import Session
from sqlalchemy import select

from models import City, Temperature
from schemas import CityCreate, TemperatureCreate


def get_all_cities(session: Session):
    return session.scalars(select(City)).all()


def get_city_by_id(session: Session, city_id: int):
    return session.scalar(select(City).where(City.id == city_id))


def create_city(session: Session, city_data: CityCreate):
    city = City(**city_data.model_dump())
    session.add(city)
    session.commit()
    session.refresh(city)

    return city


def delete_city(session: Session, city_id: int):
    city = get_city_by_id(session, city_id)

    if city is None:
        return False

    session.delete(city)
    session.commit()
    return True


def update_city(session: Session, city_id: int, city_data: CityCreate):
    city = get_city_by_id(session, city_id)
    if city is None:
        return None

    city.name = city_data.name
    city.additional_info = city_data.additional_info
    session.commit()
    session.refresh(city)

    return city


def create_temperature(session: Session, temperature_data: TemperatureCreate):
    temperature = Temperature(**temperature_data.model_dump())
    session.add(temperature)
    session.commit()
    session.refresh(temperature)

    return temperature


def get_temperatures(session: Session, city_id: int | None = None):
    if city_id is not None:
        return session.scalars(select(Temperature).where(Temperature.city_id == city_id)).all()

    return session.scalars(select(Temperature)).all()


