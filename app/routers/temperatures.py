from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.models.temperature import Temperature
from app.models.city import City
from app.schemas.temperature import TemperatureCreate, TemperatureRead
from app.services.weather import fetch_temperature

router = APIRouter(prefix="/temperatures", tags=["Temperatures"])


@router.post(
    "",
    response_model=TemperatureRead,
    status_code=status.HTTP_201_CREATED,
)
def create_temperature(
    temperature_in: TemperatureCreate,
    db: Session = Depends(get_db),
):
    city = db.query(City).filter(City.id == temperature_in.city_id).first()
    if not city:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found",
        )

    temperature = Temperature(**temperature_in.model_dump())
    db.add(temperature)
    db.commit()
    db.refresh(temperature)

    return temperature


@router.get(
    "",
    response_model=list[TemperatureRead],
)
def get_temperatures(
    city_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
):
    query = db.query(Temperature)

    if city_id is not None:
        query = query.filter(Temperature.city_id == city_id)

    return query.order_by(Temperature.date_time.desc()).all()


@router.get(
    "/{temperature_id}",
    response_model=TemperatureRead,
)
def get_temperature(
    temperature_id: int,
    db: Session = Depends(get_db),
):
    temperature = db.query(Temperature).filter(
        Temperature.id == temperature_id
    ).first()

    if not temperature:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Temperature record not found",
        )

    return temperature


@router.delete(
    "/{temperature_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_temperature(
    temperature_id: int,
    db: Session = Depends(get_db),
):
    temperature = db.query(Temperature).filter(
        Temperature.id == temperature_id
    ).first()

    if not temperature:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Temperature record not found",
        )

    db.delete(temperature)
    db.commit()


@router.post(
    "/update",
    status_code=status.HTTP_201_CREATED,
)
async def update_temperatures(
    db: Session = Depends(get_db),
):
    cities = db.query(City).all()

    if not cities:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No cities found",
        )

    created_records = 0

    for city in cities:
        temperature_value = await fetch_temperature(city.name)

        if temperature_value is None:
            continue

        temperature = Temperature(
            city_id=city.id,
            temperature=temperature_value,
            date_time=datetime.now(timezone.utc),
        )

        db.add(temperature)
        created_records += 1

    db.commit()

    return {
        "message": "Temperature update completed",
        "records_created": created_records,
    }
