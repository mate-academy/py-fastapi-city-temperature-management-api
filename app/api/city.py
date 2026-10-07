from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_db
from app.crud import city as crud
from app.schemas.city import City, CityCreate, CityUpdate

router = APIRouter(prefix="/cities", tags=["cities"])


@router.post("", response_model=City, status_code=status.HTTP_201_CREATED)
async def create_city(
        city: CityCreate,
        db: AsyncSession = Depends(get_db),
):
    try:
        return await crud.create_city(db, city)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="City with this name already exists",
        )


@router.get("", response_model=list[City])
async def read_cities(db: AsyncSession = Depends(get_db)):
    return await crud.get_cities(db)


@router.get("/{city_id}", response_model=City)
async def read_city(city_id: int, db: AsyncSession = Depends(get_db)):
    db_city = await crud.get_city(db, city_id)
    if db_city is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found",
        )
    return db_city


@router.put("/{city_id}", response_model=City)
async def update_city(
        city_id: int,
        city: CityUpdate,
        db: AsyncSession = Depends(get_db),
):
    db_city = await crud.get_city(db, city_id)
    if db_city is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found",
        )
    try:
        return await crud.update_city(db, db_city, city)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="City with this name already exists",
        )


@router.delete("/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)):
    db_city = await crud.get_city(db, city_id)
    if db_city is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found",
        )
    await crud.delete_city(db, db_city)
