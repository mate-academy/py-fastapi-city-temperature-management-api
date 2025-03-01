from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound

from city.crud import (
    create_city,
    get_all_cities,
    get_city_by_id,
    delete_city_by_id,
    update_city_by_id
)
from city.schemas import CityCreate, City
from database import SessionLocal

router = APIRouter()


async def get_db():
    async with SessionLocal() as session:
        yield session


@router.post("/cities", response_model=City)
async def create_city_endpoint(city: CityCreate, db: AsyncSession = Depends(get_db)):
    return await create_city(db=db, city=city)


@router.get("/cities", response_model=list[City])
async def get_all_cities_endpoint(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    return await get_all_cities(db=db, skip=skip, limit=limit)


@router.get("/cities/{city_id}", response_model=City)
async def get_city_by_id_endpoint(city_id: int, db: AsyncSession = Depends(get_db)):
    try:
        return await get_city_by_id(db=db, city_id=city_id)
    except NoResultFound:
        raise HTTPException(status_code=404, detail=f"City with id {city_id} not found.")


@router.delete("/cities/{city_id}", status_code=204)
async def delete_city_by_id_endpoint(city_id: int, db: AsyncSession = Depends(get_db)):
    try:
        await delete_city_by_id(db=db, city_id=city_id)
    except NoResultFound:
        raise HTTPException(status_code=404, detail=f"City with id {city_id} not found.")


@router.put("/cities/{city_id}", response_model=City)
async def update_city_by_id_endpoint(
        city_id: int, updated_city: CityCreate, db: AsyncSession = Depends(get_db)
):
    """
    Update a specific city's data by its ID.

    Args:
        city_id (int): ID of the city to update.
        updated_city (CityCreate): The updated data for the city.
        db (AsyncSession): Database session.

    Returns:
        City: The updated city instance.
    """
    try:
        return await update_city_by_id(db=db, city_id=city_id, updated_data=updated_city)
    except NoResultFound:
        raise HTTPException(status_code=404, detail=f"City with id {city_id} not found.")
