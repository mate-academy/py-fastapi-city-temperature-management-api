from sqlalchemy import select
from sqlalchemy.orm import Session

import models
from models import Temperature


def create_temperature(db: Session, data: dict) -> models.Temperature:
    db_temperature = Temperature(**data)

    db.add(db_temperature)
    db.commit()
    db.refresh(db_temperature)
    return db_temperature

def get_temperature(db: Session, city_id: int | None=None):
    stmt = select(Temperature)

    if city_id is not None:
        stmt = stmt.where(Temperature.city_id == city_id)
    result = db.scalars(stmt).all()
    return result
