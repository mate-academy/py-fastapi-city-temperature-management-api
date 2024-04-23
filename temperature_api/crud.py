from sqlalchemy.orm import Session
from temperature_api import models


def cities_temperatures(db: Session, city_id: int):
    result = db.query(models.Temperature)
    if city_id:
        return result.filter(models.Temperature.city_id == city_id)
    return result.all()


def update_city_temperature(
        city_id: int,
        temperature: float,
        db: Session
):
    city_data = (db.query(models.Temperature)
                 .filter(models.Temperature.city_id == city_id).first())
    if city_data:
        city_data.temperature = temperature
    else:
        city_data = models.Temperature(
            city_id=city_id,
            temperature=temperature
        )
        db.add(city_data)
    db.commit()
    db.refresh(city_data)
    return city_data
