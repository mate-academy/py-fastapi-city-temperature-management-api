import httpx
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.services.weather import WeatherServiceError, fetch_current_temperature

router = APIRouter(prefix="/temperatures", tags=["temperatures"])


@router.post("/update", response_model=schemas.TemperatureUpdateResult)
async def update_temperatures(db: Session = Depends(get_db)):
    cities = db.query(models.City).order_by(models.City.id).all()

    if not cities:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No cities found",
        )

    updated: list[models.Temperature] = []
    errors: list[str] = []

    for city in cities:
        try:
            current_temperature = await fetch_current_temperature(city.name)
        except (httpx.HTTPError, WeatherServiceError) as exc:
            errors.append(f"{city.name}: {exc}")
            continue

        temperature = models.Temperature(
            city_id=city.id,
            date_time=current_temperature.measured_at,
            temperature=current_temperature.temperature,
        )
        db.add(temperature)
        updated.append(temperature)

    if not updated:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail={"message": "Could not update temperatures", "errors": errors},
        )

    db.commit()

    for temperature in updated:
        db.refresh(temperature)

    return {"updated": updated, "errors": errors}


@router.get("", response_model=list[schemas.Temperature])
def read_temperatures(
    city_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
):
    query = db.query(models.Temperature)

    if city_id is not None:
        city = db.get(models.City, city_id)

        if city is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="City not found",
            )

        query = query.filter(models.Temperature.city_id == city_id)

    return query.order_by(models.Temperature.date_time.desc()).all()
