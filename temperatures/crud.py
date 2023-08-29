from datetime import datetime

from sqlalchemy.orm import Session

from cities.crud import read_all_cities
from temperatures.models import TemperatureDB
from temperatures.schemas import TemperatureCreate
from utils import get_temperature


def create_temperature(db: Session, temperature: TemperatureCreate):
    db_temperature = TemperatureDB(
        city_id=temperature.city_id,
        date_time=temperature.date_time,
        temperature=temperature.temperature,
    )
    db.add(db_temperature)
    db.commit()
    db.refresh(db_temperature)

    return db_temperature


def read_all_temperatures(
    db: Session, city_id: int | None = None, skip: int = 0, limit: int = 10
):
    queryset = db.query(TemperatureDB)

    if city_id is not None:
        queryset = queryset.filter(TemperatureDB.city_id == city_id)

    return (
        queryset.order_by(TemperatureDB.date_time.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def update_all_city_temperatures(db: Session):
    cities = read_all_cities(db=db)
    updated_temperatures = []

    for city in cities:
        print(f"Updated temperature in {city.name}")

        temperature_data = {
            "city_id": city.id,
            "date_time": datetime.now(),
            "temperature": get_temperature(city=city.name),
        }
        temperature = TemperatureCreate(**temperature_data)
        updated_temperatures.append(
            create_temperature(db=db, temperature=temperature)
        )

    return updated_temperatures
