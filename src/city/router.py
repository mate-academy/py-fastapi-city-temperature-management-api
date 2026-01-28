from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from src.city.schemas import CityCreateSchema, CityRead
from src.dependencies import get_db
from src.city import crud

router = APIRouter()


@router.get("/cities", response_model=list[CityRead])
async def read_cities(db: Annotated[AsyncSession, Depends(get_db)]):
    return await crud.get_cities(db)


@router.post(
    "/cities",
    response_model=CityRead,
    status_code=status.HTTP_201_CREATED
)
async def create_city(
        city: CityCreateSchema,
        db: Annotated[AsyncSession, Depends(get_db)]
):
    return await crud.create_city(db=db, city_data=city)


@router.get("/cities/{city_id}", response_model=CityRead)
async def read_city(
        city_id: int,
        db: Annotated[AsyncSession, Depends(get_db)]
):
    city = await crud.get_city_by_id(db=db, city_id=city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@router.put("/cities/{city_id}", response_model=CityRead)
async def update_city(
        city_id: int,
        name: str,
        additional_info: str,
        db: Annotated[AsyncSession, Depends(get_db)]
):
    city = await crud.update_city_by_id(
        db=db,
        city_id=city_id,
        name=name,
        additional_info=additional_info
    )

    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@router.delete("/cities/{city_id}", response_model=CityRead)
async def delete_city(
        city_id: int,
        db: Annotated[AsyncSession, Depends(get_db)]
):
    city = await crud.delete_city(db=db, city_id=city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city
