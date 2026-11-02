from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from temperatures import models


def get_temperatures(db_session: Session, city_id: int | None = None) -> list[models.Temperature]:
    queryset = select(models.Temperature)
    if city_id is not None:
        queryset = queryset.where(models.Temperature.city_id == city_id)
    return list(db_session.scalars(queryset).all())


def create_temperatures(db_session: Session, city_temp_dict: dict):
    now = datetime.now(timezone.utc)
    records = [
        models.Temperature(
            city_id=city_id,
            date_time=now,
            temperature=temp
        )
        for city_id, temp in city_temp_dict.items() if temp is not None
    ]
    db_session.add_all(records)
    db_session.commit()
    return records
