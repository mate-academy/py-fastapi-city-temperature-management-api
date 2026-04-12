from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from crud.city import get_cities
from database import get_db
from schemas.temperature import TemperatureRead
import crud.temperature as crud_temperature
from services.weather import fetch_temperature

router = APIRouter()

@router.post("/update", response_model=list[TemperatureRead])
async def update_temperature(db: Session = Depends(get_db)):
    cities = get_cities(db)

    results = []
    for city in cities:
        temp = await fetch_temperature(city.name)

        record = crud_temperature.create_temperature(
            db,
            {
                "city_id": city.id,
                "datetime": datetime.now(timezone.utc),
                "temperature": temp,
            },
        )

        results.append(record)

    return results

@router.get("/", response_model=list[TemperatureRead])
def read_temperatures(
    city_id: int | None = None,
    db: Session = Depends(get_db),
):
    return crud_temperature.get_temperature(db, city_id)
