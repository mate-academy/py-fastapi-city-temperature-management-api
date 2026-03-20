from sqlalchemy.orm import Session

from temperature import models


def get_temperatures(db: Session, city_id: int = None):
    query = db.query(models.Temperature)
    if city_id:
        query = query.filter(models.Temperature.city_id == city_id)
    return query.all()


def create_temperature(db: Session, city_id: int, temperature: float, date_time):
    db_temp = models.Temperature(
        city_id=city_id,
        temperature=temperature,
        date_time=date_time
    )
    db.add(db_temp)
    db.commit()
    db.refresh(db_temp)
    return db_temp
