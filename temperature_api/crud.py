from datetime import datetime
from sqlalchemy.orm import Session

from city_api.models import City as CityModel
from temperature_api.schemas import TemperatureCreate


def create_temperature_record(
    db: Session, city_name: str, temperature: float
) -> TemperatureCreate:
    city = (
        db.query(CityModel).filter(
            CityModel.name == city_name
        ).first()
    )
    temperature_data = TemperatureCreate(
        city_id=city.id,
        date_time=datetime.utcnow(),
        temperature=temperature
    )
    return temperature_data
