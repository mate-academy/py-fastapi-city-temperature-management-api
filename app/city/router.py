from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.city import crud, models, schemas
from app.dependencies import get_db

router = APIRouter(prefix="/cities", tags=["cities"])


async def get_city_or_404(
    city_id: int, db: AsyncSession = Depends(get_db)
) -> models.City:
    db_city = await crud.get_city(db, city_id)
    if db_city is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"City with id={city_id} not found",
        )
    return db_city


async def ensure_name_is_free(db: AsyncSession, name: str) -> None:
    if await crud.get_city_by_name(db, name) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"City with name '{name}' already exists",
        )


@router.post(
    "", response_model=schemas.City, status_code=status.HTTP_201_CREATED
)
async def create_city(
    city: schemas.CityCreate, db: AsyncSession = Depends(get_db)
):
    await ensure_name_is_free(db, city.name)
    return await crud.create_city(db, city)


@router.get("", response_model=List[schemas.City])
async def read_cities(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db),
):
    return await crud.get_cities(db, skip=skip, limit=limit)


@router.get("/{city_id}", response_model=schemas.City)
async def read_city(db_city: models.City = Depends(get_city_or_404)):
    return db_city


@router.put("/{city_id}", response_model=schemas.City)
async def update_city(
    city: schemas.CityUpdate,
    db_city: models.City = Depends(get_city_or_404),
    db: AsyncSession = Depends(get_db),
):
    if city.name is not None and city.name != db_city.name:
        await ensure_name_is_free(db, city.name)
    return await crud.update_city(db, db_city, city)


@router.delete("/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_city(
    db_city: models.City = Depends(get_city_or_404),
    db: AsyncSession = Depends(get_db),
):
    await crud.delete_city(db, db_city)
