from sqlalchemy.orm import Session

from temperature import models


def get_all_temperatures(
    db: Session, skip: int, limit: int, city_id: int = None
) -> list[models.Temperature]:
    queryset = db.query(models.Temperature)
    if city_id is not None:
        queryset = queryset.filter(models.Temperature.city_id == city_id)

    return queryset.offset(skip).limit(limit).all()
