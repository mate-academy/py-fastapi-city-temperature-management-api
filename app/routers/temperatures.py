from datetime import datetime

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.crud.city import get_cities
from app.crud.temperature import create_temperature
from app.crud.temperature import get_temperatures
from app.crud.temperature import get_temperatures_by_city
from app.dependencies import get_db
from app.schemas.temperature import TemperatureResponse
from app.services.weather import fetch_temperature

router = APIRouter(prefix="/temperatures", tags=["temperatures"])


@router.post("/update")
async def update_temperatures(db: Session = Depends(get_db)):
    cities = get_cities(db)

    for city in cities:
        coords = _get_coords(city.name)
        if not coords:
            continue

        temp = await fetch_temperature(coords["lat"], coords["lon"])

        create_temperature(
            db,
            city_id=city.id,
            date_time=datetime.utcnow(),
            temperature=temp,
        )

    return {"detail": "updated"}


@router.get("", response_model=list[TemperatureResponse])
def read_all(db: Session = Depends(get_db)):
    return get_temperatures(db)


@router.get("/", response_model=list[TemperatureResponse])
def read_by_city(city_id: int, db: Session = Depends(get_db)):
    return get_temperatures_by_city(db, city_id)


def _get_coords(city_name: str):
    mapping = {
        "Kyiv": {"lat": 50.4501, "lon": 30.5234},
        "Lviv": {"lat": 49.8397, "lon": 24.0297},
        "Odesa": {"lat": 46.4825, "lon": 30.7233},
        "Kharkiv": {"lat": 49.9935, "lon": 36.2304},
    }
    return mapping.get(city_name)
