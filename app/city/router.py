from collections.abc import Sequence

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.city import crud, models, schemas
from app.services.city_weather_service import FindCityService
from core import get_db

city_router = APIRouter(prefix="/cities", tags=["City"])


@city_router.get("/", response_model=list[schemas.City])
async def list_cities(
    db: AsyncSession = Depends(get_db), skip: int = 0, limit: int = 100
) -> Sequence[models.City]:
    """Retrieves a list of all cities."""
    cities = await crud.get_cities(db, skip=skip, limit=limit)

    return cities


@city_router.get("/{city_id}/", response_model=schemas.City)
async def get_city_by_id(
    city_id: int, db: AsyncSession = Depends(get_db)
) -> models.City:
    """Retrieves a specific city by its ID."""
    crud.check_city_existence(
        city_id=city_id, city=(city := await crud.get_city_by_id(db, city_id=city_id))
    )

    return city


@city_router.post("/", response_model=schemas.City, status_code=status.HTTP_201_CREATED)
async def create_city(
    city_data: schemas.CityCreate,
    city_service: FindCityService = Depends(),
    db: AsyncSession = Depends(get_db),
) -> models.City:
    """Creates a new city."""
    new_city = await crud.create_city(
        db, city_data=await city_service.refine_city_name(city_data)
    )

    return new_city


@city_router.put("/{city_id}/", response_model=schemas.City)
async def update_city(
    city_id: int,
    update_data: schemas.CityUpdate,
    city_service: FindCityService = Depends(),
    db: AsyncSession = Depends(get_db),
) -> models.City:
    """Updates an existing city."""
    if update_data.name:
        update_data = await city_service.refine_city_name(update_data)

    db_city = await crud.update_city(db, city_id=city_id, update_data=update_data)

    return db_city


@city_router.delete("/{city_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)) -> None:
    """Deletes a city by its ID."""
    await crud.delete_city(db, city_id=city_id)
