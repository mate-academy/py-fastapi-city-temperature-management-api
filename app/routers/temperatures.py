import asyncio

import httpx
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.dependencies import get_db
from app.services.weather import fetch_temperature


router = APIRouter(
    prefix="/temperatures",
    tags=["temperatures"],
)


@router.post(
    "/update",
    response_model=schemas.TemperatureUpdateResult,
)
async def update_temperatures(
    db: Session = Depends(get_db),
) -> schemas.TemperatureUpdateResult:
    cities = crud.get_cities(
        db,
        skip=0,
        limit=10000,
    )

    if not cities:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No cities found in the database",
        )

    async with httpx.AsyncClient(timeout=10.0) as client:
        tasks = [
            fetch_temperature(
                client,
                city.id,
                city.name,
            )
            for city in cities
        ]

        results = await asyncio.gather(
            *tasks,
            return_exceptions=True,
        )

    created = []
    errors = []

    for city, result in zip(cities, results):
        if isinstance(result, Exception):
            errors.append(
                f"{city.name}: {result}"
            )
            continue

        created.append(
            crud.create_temperature(
                db,
                result,
            )
        )

    if not created:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail={
                "message": "Could not update any temperatures",
                "errors": errors,
            },
        )

    return schemas.TemperatureUpdateResult(
        created=created,
        errors=errors,
    )


@router.get(
    "",
    response_model=list[schemas.Temperature],
)
def read_temperatures(
    skip: int = 0,
    limit: int = 100,
    city_id: int | None = None,
    db: Session = Depends(get_db),
) -> list[schemas.Temperature]:
    if city_id is not None:
        city = crud.get_city(db, city_id)

        if city is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="City not found",
            )

    return crud.get_temperatures(
        db,
        skip=skip,
        limit=limit,
        city_id=city_id,
    )
