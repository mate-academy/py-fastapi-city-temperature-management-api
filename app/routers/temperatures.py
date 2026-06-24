import httpx
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.annotation import Annotated

from app import crud, schemas
from app.database import get_db
from app.services.weather import WeatherServiceError, fetch_temperature


router = APIRouter(prefix="/temperatures", tags=["temperatures"])


@router.post("/update", response_model=list[schemas.Temperature])
async def update_temperatures(
        db: Annotated[AsyncSession, Depends(get_db)]
):
    cities = await crud.get_cities(db)
    city_temperatures = []

    async with httpx.AsyncClient(timeout=10) as client:
        try:
            for city in cities:
                temperature = await fetch_temperature(client, city.name)
                city_temperatures.append((city.id, temperature))
        except WeatherServiceError as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=str(exc),
            )

    return await crud.create_temperatures(db, city_temperatures)


@router.get("", response_model=list[schemas.Temperature])
async def list_temperatures(
    city_id: int | None = Query(default=None),
    db: AsyncSession = Depends(get_db),
):
    if city_id is not None and await crud.get_city(db, city_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found",
        )

    return await crud.get_temperatures(db, city_id)
