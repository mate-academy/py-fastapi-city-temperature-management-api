from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from src.database.session import get_db
from src.schemas import CityCreate, City
from src.database.models.crud import (
    create_city,
    get_cities,
    get_city,
    update_city,
    delete_city,
)

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/cities", response_model=City)
async def create_city_view(city: CityCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await create_city(db, city)
    except Exception as e:
        logger.error(f"Error creating city: {e}")
        raise HTTPException(status_code=500, detail="Error creating city")


@router.get("/cities", response_model=list[City])
async def get_cities_view(db: AsyncSession = Depends(get_db)):
    try:
        return await get_cities(db)
    except Exception as e:
        logger.error(f"Error retrieving cities: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving cities")


@router.get("/cities/{city_id}", response_model=City)
async def get_city_view(city_id: int, db: AsyncSession = Depends(get_db)):
    city = await get_city(db, city_id)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@router.put("/cities/{city_id}", response_model=City)
async def update_city_view(
    city_id: int, city: CityCreate, db: AsyncSession = Depends(get_db)
):
    try:
        updated_city = await update_city(db, city_id, city)
        if updated_city is None:
            raise HTTPException(status_code=404, detail="City not found")
        return updated_city
    except Exception as e:
        logger.error(f"Error updating city {city_id}: {e}")
        raise HTTPException(status_code=500, detail="Error updating city")


@router.delete("/cities/{city_id}", response_model=City)
async def delete_city_view(city_id: int, db: AsyncSession = Depends(get_db)):
    try:
        deleted_city = await delete_city(db, city_id)
        if deleted_city is None:
            raise HTTPException(status_code=404, detail="City not found")
        return deleted_city
    except Exception as e:
        logger.error(f"Error deleting city {city_id}: {e}")
        raise HTTPException(status_code=500, detail="Error deleting city")
