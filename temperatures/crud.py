from sqlalchemy.orm import Session

from temperatures.models import DBTemperature


def get_temperatures(
        db: Session,
        city_id: int | None = None,
):
    queryset = db.query(DBTemperature)

    if city_id:
        queryset = queryset.filter(city_id == city_id)

    return queryset.all()

