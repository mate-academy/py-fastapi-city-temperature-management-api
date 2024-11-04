from sqlalchemy.orm import Session

from app.models.temperature import Temperature
from app.schemas.temperature import TemperatureCreate


def create_temperature(db: Session, temperature: TemperatureCreate):
    db_temp = Temperature(city_id=temperature.city_id, temperature=temperature.temperature)
    db.add(db_temp)
    db.commit()
    db.refresh(db_temp)
    return db_temp

def get_temperature(db: Session, city_id: int = None):
    if city_id:
        return db.query(Temperature).filter(Temperature.city_id == city_id).all()
    return db.query(Temperature).all()
