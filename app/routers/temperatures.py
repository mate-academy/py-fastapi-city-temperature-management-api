import asyncio
import httpx

from typing import Sequence

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio.session import AsyncSession

from app import crud, schemas, models
from app.dependencies import get_db
from app.models import City
from app.settings import settings

router = APIRouter(
    prefix="/temperatures",
    tags=["temperatures"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def read_temperatures(
        skip: int = 0,
        limit: int = 100,
        db: AsyncSession = Depends(get_db),
        city_id: int | None = None,
) -> Sequence[schemas.Temperature]:
    result = await crud.get_all_temperatures(
        db=db,
        city_id=city_id,
        skip=skip,
        limit=limit
    )
    return result

async def fetch_temperature_for_city(
        client: httpx.AsyncClient,
        city: City
) -> float:
    try:
        response = await client.get(
            url=f"{settings.weather_api_url}/current.json",
            params={"q": city.name, "key": settings.api_key}
        )
        response.raise_for_status()
        return response.json()["current"]["temp_c"]
    except httpx.HTTPStatusError as error:
        if error.response.status_code == 400:
            raise HTTPException(
                status_code=404,
                detail=f"City '{city.name}' not found on weather service"
            )
        raise HTTPException(
            status_code=502,
            detail=f"External API error"
        )

@router.post("/update")
async def update_temperatures_of_all_cities(
        db: AsyncSession = Depends(get_db),
) -> dict:
    cities = await crud.get_all_cities(db)

    async with httpx.AsyncClient() as client:
        results = await asyncio.gather(
            *[fetch_temperature_for_city(client, city) for city in cities],
            return_exceptions=True
        )

    for city, result in zip(cities, results):
        if isinstance(result, Exception):
            print(f"Failed to fetch temperature for {city.name}: {result}")
            continue
        temperature = models.Temperature(
            city_id=city.id,
            temperature=result
        )
        db.add(temperature)
    await db.commit()
    return {"detail": f"Updated temperatures for {len(cities)} cities"}
