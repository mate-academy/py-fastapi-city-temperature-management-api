from sqlalchemy.orm import Session
from app.temperatures import models, schemas

def get_temperatures(db: Session, city_id: int = None):
    query = db.query(models.Temperature)
    if city_id:
        query = query.filter(models.Temperature.city_id == city_id)
    return query.all()

def create_temperature_record(db: Session, temperature_in: schemas.TemperatureCreate):
    db_temp = models.Temperature(
        city_id=temperature_in.city_id,
        temperature=temperature_in.temperature,
        date_time=temperature_in.date_time
    )
    db.add(db_temp)
    db.commit()
    db.refresh(db_temp)
    return db_temp
