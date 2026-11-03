from sqlalchemy import select
from sqlalchemy.orm import Session

from app.temperatures import models


def get_temperatures(
        db: Session,
        city_id: int | None = None
) -> list[models.Temperature]:
    query = select(models.Temperature)
    query = query.order_by(models.Temperature.date_time.desc())
    if city_id is not None:
        query = query.where(models.Temperature.city_id == city_id)
    return list(db.scalars(query))


def create_temperatures(db: Session, records: list[tuple[int, float]]) -> None:
    db.add_all(
        models.Temperature(city_id=city_id, temperature=value)
        for city_id, value in records
    )
    db.commit()
