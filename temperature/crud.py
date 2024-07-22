from sqlalchemy.orm import Session
from cities.crud import get_all_cities_no_pagination
from . import models, schemas, utils
import datetime
def get_all_temperatures(db: Session, skip: int, limit: int):
    return db.query(models.Temperature).offset(skip).limit(limit).all()

def get_temperature_by_city_id(db: Session, city_id: int):
    return db.query(models.Temperature).filter(models.Temperature.city_id == city_id).first()

async def get_temperatures_for_cities(db: Session):
    cities = get_all_cities_no_pagination(db)
    print(cities)
    for city in cities:
        current_temp = await utils.get_current_temperature(city.name)
        temperature = get_temperature_by_city_id(db, city.id)
        if temperature:
            temperature.temperature = current_temp
            db.commit()

        else:
            db_temp = models.Temperature(city_id = city.id, temperature = current_temp, date_time = datetime.datetime.now())
            db.add(db_temp)
            db.commit()
            db.refresh(db_temp)

    return "temps updated"

