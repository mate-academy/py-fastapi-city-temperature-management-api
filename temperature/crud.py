from sqlalchemy.orm import Session

from db import models


def get_all_temperatures(db: Session, city_id: int = None):
    if city_id is None:
        return db.query(models.DBTemperature).all()

    return (
        db.query(models.DBTemperature)
        .filter(models.DBTemperature.city_id == city_id)
        .all()
    )
