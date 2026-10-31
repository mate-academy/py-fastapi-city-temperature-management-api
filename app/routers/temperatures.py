import asyncio
from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models import City, Temperature
from app.schemas import TemperatureResponse
from app.services.weather import get_temperature_for_city

router = APIRouter(prefix="/temperatures", tags=["Temperatures"])


@router.get("/", response_model=list[TemperatureResponse])
def get_temperatures(
    city_id: int | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(Temperature)

    if city_id is not None:
        query = query.filter(Temperature.city_id == city_id)

    return query.all()


@router.post("/update")
async def update_temperatures(db: Session = Depends(get_db)):
    cities = db.query(City).all()
    temperatures = await asyncio.gather(
        *[get_temperature_for_city(city.name) for city in cities],
        return_exceptions=True,
    )
    for city, temperature in zip(cities, temperatures):
        if isinstance(temperature, Exception):
            db.rollback()
            if isinstance(temperature, ValueError):
                raise HTTPException(status_code=404, detail=str(temperature))
            raise HTTPException(status_code=502, detail=str(temperature))

        temperature_record = Temperature(
            city_id=city.id,
            date_time=datetime.now(UTC),
            temperature=temperature,
        )
        db.add(temperature_record)
    db.commit()
    return {"message": "Temperatures updated successfully"}
