from sqlalchemy import select
from sqlalchemy.orm import Session

from city.crud import get_city_or_404
from city.models import City
from temperature.models import Temperature
from settings import settings
from datetime import datetime
import httpx


def get_temperatures_crud(db: Session, city_id: int = None):
    if city_id:
        city = get_city_or_404(db, city_id)
        return city.temperatures
    return db.scalars(select(Temperature)).all()


async def check_current_temperatures(db: Session):
    cities = db.scalars(select(City)).all()

    async with httpx.AsyncClient() as client:
        for city in cities:
            response = await client.get(
                f"https://api.openweathermap.org/data/2.5/weather?q={city.name}&appid={settings.API_KEY}&units=metric"
            )
            data = response.json()
            db_temperature = Temperature(
                city_id=city.id,
                date_time=datetime.now(),
                temperature=data["main"]["temp"]
            )
            db.add(db_temperature)
        db.commit()

    temperatures = db.scalars(select(Temperature)).all()
    return temperatures
