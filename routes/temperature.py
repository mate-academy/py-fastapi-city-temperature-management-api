from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from config.dependencies import get_db
import crud.temperature as crud
from schemas.temperature import TemperatureResponse, TemperatureUpdateResponse

router = APIRouter(prefix="/temperatures", tags=["temperature"])


@router.post("/update", status_code=200, response_model=TemperatureUpdateResponse)
async def update_temperatures(db: AsyncSession = Depends(get_db)):
    """
    Fetch current temperature for all cities from online resource
    and store in database
    """
    result = await crud.update_temperatures_for_all_cities(db)
    return result


@router.get("/", status_code=200, response_model=list[TemperatureResponse])
async def get_temperatures(
    city_id: int | None = Query(None, description="Filter by city ID"),
    db: AsyncSession = Depends(get_db),
):
    """
    Get all temperature records or filter by city_id

    - If city_id is provided: returns temperatures for that city
    - If city_id is not provided: returns all temperature records
    """
    temperatures = await crud.get_temperatures(db, city_id=city_id)

    if city_id is not None and not temperatures:
        raise HTTPException(
            status_code=404,
            detail=f"No temperature records found for city_id={city_id}",
        )

    return temperatures
