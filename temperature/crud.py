from sqlalchemy.orm import Session
import models, schemas
from utils import get_weather
from datetime import datetime
from city.models import City
from fastapi import HTTPException, status


def all_temperature(db: Session):
    return db.query(models.Temperature).all()


def all_temperature_by_city_id(db: Session, city_id: int):
    return db.query(models.Temperature).filter(models.Temperature.city_id == city_id).all()


async def update_all_city_temperature(db: Session):
    cities = db.query(City).all()

    for city in cities:
        try:
            temperature_result = await get_weather(city.name)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error fetching temperature for {city.name}: {str(e)}",
            )

        db_temperature = models.Temperature(
            city_id=city.id,
            date_time=datetime.now(),
            temperature=temperature_result,
        )

        db.add(db_temperature)
        db.commit()
        db.refresh(db_temperature)

    return True
