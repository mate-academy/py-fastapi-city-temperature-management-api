from typing import List
import httpx
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from . import models, schemas
from city_crud_api.models import City


def create_temperature(
    db: Session, temperature: schemas.TemperatureCreate
) -> models.Temperature:
    db_temperature = models.Temperature(**temperature.dict())
    db.add(db_temperature)
    db.commit()
    db.refresh(db_temperature)
    return db_temperature


def get_all_temperatures(
    db: Session, skip: int = 0, limit: int = 10
) -> List[models.Temperature]:
    return db.query(models.Temperature).offset(skip).limit(limit).all()


def get_temperatures_by_city(
    db: Session, city_id: int
) -> List[models.Temperature]:
    return (
        db.query(models.Temperature)
        .filter(models.Temperature.city_id == city_id)
        .all()
    )


async def fetch_city_temperature(
    client: httpx.AsyncClient, city: City, api_key: str
) -> schemas.TemperatureCreate:
    try:
        response = await client.get(
            f"http://api.weatherapi.com/v1/"
            f"current.json?key={api_key}&q={city.name}&aqi=no"
        )
        response.raise_for_status()
        data = response.json()
    except httpx.HTTPStatusError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error fetching weather data for city {city.name}",
        )
    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error requesting weather data: {str(exc)}",
        )

    return schemas.TemperatureCreate(
        city_id=city.id,
        date_time=data["current"]["last_updated"],
        temperature=data["current"]["temp_c"],
    )
