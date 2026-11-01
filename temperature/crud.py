from sqlalchemy.orm import Session

from city.models import DBCity

from temperature.utils import get_all_city_names
from temperature.weather_scrapper import scrap_cities_weather
from temperature import schemas
from  temperature.models import DBTemperature


async def sync_temperature(db: Session):
    cities = get_all_city_names(db)
    updated_temperature = await scrap_cities_weather(cities)

    for temperature in updated_temperature:
        if not temperature:
            continue

        db_city = db.query(DBCity).filter(DBCity.name == temperature["city"]).first()

        if not db_city:
            continue

        new_temperature = schemas.TemperatureCreate(
            city_id=db_city.id,
            temperature=temperature["temperature"],
            date_time=temperature["temperature_time"],
        )

        db_temperature = DBTemperature(**new_temperature.model_dump())
        db.add(db_temperature)
        db.commit()

        db.refresh(db_temperature)


    return "Temperatures updated."
