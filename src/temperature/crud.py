from sqlalchemy.orm import Session
from .models import DBTemperature

from .utils import get_temperature_for_all_cities, update_or_create_temperature


def get_temperature_list(
        db: Session,
        skip: int,
        limit: int,
        city_id: int | None = None
) -> list[DBTemperature] | DBTemperature | None:
    temperatures = db.query(DBTemperature)

    if city_id:
        temperatures = temperatures.filter(DBTemperature.city_id == city_id).first()

    return temperatures.offset(skip).limit(limit).all()


async def update_cities_temperature(db: Session) -> list[DBTemperature]:
    data_to_update = await get_temperature_for_all_cities(db=db)

    for city, temperature in data_to_update:
        await update_or_create_temperature(
            db=db, city_id=city.id, temperature=temperature
        )
    db.commit()
    return db.query(DBTemperature).all()
