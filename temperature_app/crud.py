import asyncio

from sqlalchemy.orm import Session

import city_app.models
import temperature_app.models
from temperature_app.utils import fetch_temperatures


def update_temperatures(db: Session):
    cities = db.query(city_app.models.City).all()
    fetched_temperatures = asyncio.run(fetch_temperatures(cities, db))

    return fetched_temperatures


def get_temperatures(db: Session, city_id: int | None = None):
    queryset = db.query(temperature_app.models.Temperature)

    if city_id is not None:
        queryset = queryset.filter(temperature_app.models.Temperature.city_id == city_id)

    return queryset.all()
