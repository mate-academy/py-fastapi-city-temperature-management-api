from fastapi import BackgroundTasks
from sqlalchemy.orm import Session

from temperature import models as temperature_models
from backgroud_tasks import update_weather_data
from cities import models as cities_models


def get_temperature(
        db: Session,
        city_id: int
) -> temperature_models.Temperature:
    return db.query(temperature_models.Temperature).filter(
        temperature_models.Temperature.city_id == city_id
    ).first()


def get_temperatures(
        db: Session,
        skip: int = 0,
        limit: int = 100
) -> list[temperature_models.Temperature]:
    return (db.query(temperature_models.Temperature)
            .offset(skip).limit(limit).all())


async def create_city_temperature(
        db: Session,
        city: cities_models.City,
        background_tasks: BackgroundTasks
) -> None:
    db_temperature = temperature_models.Temperature(city_id=city.id)
    db.add(db_temperature)
    db.commit()
    db.refresh(db_temperature)
    background_tasks.add_task(
        update_weather_data,
        city=city,
        temperature_id=db_temperature.id,
        db=db,
        background_tasks=background_tasks
    )


async def update_temperatures(
        db: Session,
        background_tasks: BackgroundTasks
) -> None:
    db_cities = db.query(cities_models.City).all()

    for city in db_cities:
        background_tasks.add_task(
            update_weather_data,
            city=city,
            temperature_id=city.temperature.id,
            db=db,
            background_tasks=background_tasks
        )
