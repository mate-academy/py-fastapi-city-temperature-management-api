from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.cities import crud
from app.cities.schemas import CityCreate, CityRead, CityUpdate

router = APIRouter(prefix="/cities", tags=["Cities"])


@router.post("/", response_model=CityRead, status_code=status.HTTP_201_CREATED)
async def create_city(
    city_data: CityCreate,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    return await crud.create_city(db, city_data)

@router.get("/", response_model=list[CityRead])
async def read_cities(
    db: Annotated[AsyncSession, Depends(get_db)]
):
    return await crud.get_cities(db)


@router.get("/{city_id}", response_model=CityRead)
async def read_city(
    city_id: int,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    city = await crud.get_city_by_id(db, city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@router.put("/{city_id}", response_model=CityRead)
async def update_city(
    city_id: int,
    city_data: CityUpdate,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    city = await crud.get_city_by_id(db, city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return await crud.update_city(db, city, city_data)


@router.delete("/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_city(
    city_id: int,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    city = await crud.get_city_by_id(db, city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    await crud.delete_city(db, city)
