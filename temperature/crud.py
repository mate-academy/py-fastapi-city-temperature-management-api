from sqlalchemy import select
from sqlalchemy.orm import Session

from temperature import models


def get_temperature(db: Session, city_id: int | None = None):
    query = select(models.Temperature)

    if city_id is not None:
        query = query.where(models.Temperature.city_id == city_id)

    return db.scalars(query).all()
