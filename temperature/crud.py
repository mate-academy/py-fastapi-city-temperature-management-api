from sqlalchemy.orm import Session

from temperature.models import TemperatureDB


def get_all_temperatures(db: Session) -> list[TemperatureDB]:
    return db.query(TemperatureDB).all()


def get_temperatures_by_city(city_id: int, db: Session) -> list[TemperatureDB]:
    return db.query(TemperatureDB).filter(
        TemperatureDB.city_id == city_id
    ).all()
