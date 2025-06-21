from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from database import get_db
from temperature import crud, schemas

router = APIRouter(prefix="/temperatures", tags=["Temperatures"])


@router.get("/", response_model=List[schemas.TemperatureResponse])
async def get_all_temperatures(
    city_id: Optional[int] = None, db: AsyncSession = Depends(get_db)
):
    """
    Retrieve all temperature records. Optionally filter by city ID.
    :param city_id: Optional[int] - The ID of the city to filter temperatures.
    :param db: AsyncSession - The database session.
    :return: List[schemas.TemperatureResponse] - A list of temperature records.
    """
    return await crud.get_temperatures(db, city_id)


@router.post("/update", response_model=dict)
async def update_temperatures(db: AsyncSession = Depends(get_db)):
    """
    Fetches and updates temperature data for all cities in the database.
    :param db: AsyncSession - The database session.
    :return: dict - A success message after updating temperatures.
    """
    await crud.update_temperatures(db)
    return {"message": "Temperatures updated successfully"}
