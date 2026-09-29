from typing import List, Optional

import httpx
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.city import crud as city_crud
from app.dependencies import get_db, get_http_client
from app.temperature import crud, schemas

router = APIRouter(prefix="/temperatures", tags=["temperatures"])


@router.post("/update", response_model=schemas.TemperatureUpdateResult)
async def update_temperatures(
    db: AsyncSession = Depends(get_db),
    client: httpx.AsyncClient = Depends(get_http_client),
):
    """Fetch the current temperature for every city and store it."""
    return await crud.update_temperatures(db, client)


@router.get("/", response_model=List[schemas.Temperature])
async def read_temperatures(
    city_id: Optional[int] = Query(
        None, description="Return records only for this city"
    ),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db),
):
    if city_id is not None and await city_crud.get_city(db, city_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"City with id={city_id} not found",
        )
    return await crud.get_temperatures(
        db, city_id=city_id, skip=skip, limit=limit
    )
