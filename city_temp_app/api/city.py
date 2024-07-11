from typing import Any, Sequence

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import CursorResult

from sqlalchemy.ext.asyncio import AsyncSession

from city_temp_app import crud, schemas
from city_temp_app.database import get_db
from city_temp_app.models import City

router = APIRouter()


@router.post("/cities/", response_model=schemas.City)
async def create_city(
        city: schemas.CityCreate, db: AsyncSession = Depends(get_db)
) -> dict[str, CursorResult[Any]]:
    return await crud.create_city(db, city)


@router.get("/cities/", response_model=list[schemas.City])
async def read_cities(db: AsyncSession = Depends(get_db)) -> Sequence[City]:
    return await crud.read_cities(db)


@router.get("/cities/{city_id}/", response_model=schemas.City)
async def read_city_by_id(
        city_id: int, db: AsyncSession = Depends(get_db)
) -> HTTPException | City:
    city = await crud.read_city_by_id(db, city_id)
    if not city:
        return HTTPException(status_code=404, detail="City not found!")

    return city


@router.delete("cities/{city_id}/", response_model=schemas.City)
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)):
    city = await crud.delete_city(db, city_id)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return city
