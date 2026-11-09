import crud
import schemas
import httpx
import asyncio
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from db.engine import get_db


router = APIRouter(
    prefix="/temperatures",
    tags=["Temperatures"]
)


@router.get("/", response_model=list[schemas.TemperatureResponse])
def get_all_temperatures(
        city_id: int | None = None,
        skip: int = Query(default=0, ge=0),
        limit: int = Query(default=10, ge=1, le=100),
        database: Session = Depends(get_db)
):
    return crud.get_all_temperatures(
        database,
        skip,
        limit,
        city_id
    )


@router.get("/{temperature_id}/", response_model=schemas.TemperatureResponse)
def get_temperature_by_id(
        temperature_id: int,
        database: Session = Depends(get_db)
):
    temperature = crud.get_temperature_by_id(
        database,
        temperature_id
    )

    if temperature is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Temperature record not found"
        )

    return temperature


@router.post(
    "/",
    response_model=schemas.TemperatureResponse,
    status_code=status.HTTP_201_CREATED
)
def create_temperature(
        temperature: schemas.TemperatureCreate,
        database: Session = Depends(get_db)
):
    return crud.create_temperature(database, temperature)


async def fetch_temperature(client, latitude, longitude):
    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m",
        "timezone": "auto"
    }

    response = await client.get(url, params=params)
    response.raise_for_status()

    data = response.json()

    return data["current"]["temperature_2m"], data["current"]["time"]


@router.post(
    "/update",
    response_model=list[schemas.TemperatureResponse]
)
async def update_temperatures(
        database: Session = Depends(get_db)
):
    cities = crud.get_all_cities(database, skip=0, limit=10000)

    if not cities:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No cities found"
        )

    temperatures = []

    try:
        async with httpx.AsyncClient() as client:
            results = await asyncio.gather(
                *[
                    fetch_temperature(
                        client,
                        city.latitude,
                        city.longitude
                    )
                    for city in cities
                ]
            )

            for city, (temperature_value, recorded_time) in zip(cities, results):
                temperature = schemas.TemperatureCreate(
                    city_id=city.id,
                    date_time=datetime.fromisoformat(recorded_time),
                    temperature=temperature_value
                )

                saved_temperature = crud.create_temperature(
                    database,
                    temperature
                )

                temperatures.append(saved_temperature)

    except (httpx.HTTPError, KeyError, ValueError) as error:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Weather API error: {str(error)}"
        )

    return temperatures
