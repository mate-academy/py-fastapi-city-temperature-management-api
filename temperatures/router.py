from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from cities.models import DBCity
from dependencies import get_db
from temperatures import schemas
from temperatures.crud import get_temperatures
from temperatures.models import DBTemperature
from weather import get_weather

router = APIRouter()


@router.post("/temperatures/update/")
async def update_temperatures(db: Session = Depends(get_db)):
    cities = db.query(DBCity).all()

    for city in cities:
        weather_date = get_weather(city.name)

        if weather_date:
            temperature = DBTemperature(
                city_id=city.id,
                date_time=datetime.now(),
                temperature=weather_date
            )
            db.add(temperature)

    db.commit()

    return {"message": "Temperatures update successfully"}


@router.get("/temperatures/", response_model=list[schemas.Temperature])
def read_temperatures(
        city_id: int | None = None,
        db: Session = Depends(get_db)
):
    return get_temperatures(db, city_id=city_id)

