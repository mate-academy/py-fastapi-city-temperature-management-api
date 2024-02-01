from sqlalchemy.orm import Session
from .models import DBTemperature

from .utils import get_temperature_for_all_cities, update_or_create_temperature


def get_temperature_list(
        db: Session,
        skip: int,
        limit: int,
) -> list[DBTemperature]:
    temperatures = db.query(DBTemperature)

    return temperatures.offset(skip).limit(limit).all()


def get_temperature_for_a_city(db: Session, city_id: int) -> DBTemperature | None:
    return db.query(DBTemperature).filter(DBTemperature.city_id == city_id).first()


async def update_cities_temperature(db: Session) -> list[DBTemperature]:
    data_to_update = await get_temperature_for_all_cities(db=db)

    for city, temperature in data_to_update:
        await update_or_create_temperature(
            db=db, city_id=city.id, temperature=temperature
        )
    db.commit()
    return db.query(DBTemperature).all()
