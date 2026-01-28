from sqlalchemy.orm import Session
from sqlalchemy import select

from models.temperature import Temperature

def create_temperature(db: Session, city_id: int, value: float):
    temp = Temperature(city_id=city_id, temperature=value)
    db.add(temp)
    db.commit()
    db.refresh(temp)
    return temp


def get_temperatures(db: Session, city_id: int | None = None):
    stmt = select(Temperature)
    if city_id is not None:
        stmt = stmt.where(Temperature.city_id == city_id)
    return db.scalars(stmt).all()
