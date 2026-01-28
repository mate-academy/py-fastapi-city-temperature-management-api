from sqlalchemy import select
from sqlalchemy.orm import Session

from models.temperature import Temperature

def add_temperature(db: Session, city_id: int, temp: float) -> Temperature:
    rec = Temperature(city_id=city_id, temperature=temp)
    db.add(rec)
    db.commit()
    db.refresh(rec)
    return rec

def list_temperatures(db: Session, city_id: int | None = None) -> list[Temperature]:
    stmt = select(Temperature).order_by(Temperature.date_time.desc())
    if city_id is not None:
        stmt = stmt.where(Temperature.city_id == city_id)
    return list(db.scalars(stmt).all())
