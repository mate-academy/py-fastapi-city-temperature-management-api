from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from city.models import City
from temperature.models import Temperature


def create_temperature_instance(
    db: AsyncSession, city: City, weather_data: float
) -> None:
    temperature_instance = Temperature(
        city_id=city.id, temperature=weather_data, date_time=datetime.now()
    )
    db.add(temperature_instance)


def update_temperature_instance(
    temperature_instance: Temperature, weather_data: float
) -> None:
    temperature_instance.temperature = weather_data
    temperature_instance.date_time = datetime.now()
