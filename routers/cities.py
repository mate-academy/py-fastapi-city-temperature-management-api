from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

import schemas, models, crud
from deps import get_session

router = APIRouter(prefix="/cities", tags=["Cities"])


@router.post("", response_model=schemas.CityResponse)
async def create_city(
    city: schemas.CityCreate,
    session: AsyncSession = Depends(get_session),
):
    db_city = models.City(**city.model_dump())
    return await crud.create_city(session, db_city)


@router.get("", response_model=List[schemas.CityResponse])
async def get_cities(session: AsyncSession = Depends(get_session)):
    return await crud.get_cities(session)


@router.delete("/{city_id}", status_code=204)
async def delete_city(
    city_id: int,
    session: AsyncSession = Depends(get_session),
):
    try:
        await crud.delete_city(session, city_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="City not found")
