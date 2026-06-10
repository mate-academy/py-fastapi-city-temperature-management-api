from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from city import schemas, crud


router = APIRouter(
    prefix="/cities",
    tags=["cities"]
)

@router.post("/", response_model=schemas.CityRead)
async def create_city(
    city: schemas.CityCreate,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    return await crud.create_city(
        db=db,
        city=city
    )


@router.get("/", response_model=list[schemas.CityRead])
async def read_all_cities(
    db: Annotated[AsyncSession, Depends(get_db)],
    skip: int = 0,
    limit: int = 10
):
    return await crud.get_cities(
        db=db,
        skip=skip,
        limit=limit
    )


@router.get("/{city_id}", response_model=schemas.CityRead)
async def read_single_city(
    city_id: int,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    db_city = await crud.get_city_by_id(db=db, city_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    
    return db_city


@router.delete("/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_city(
    city_id: int,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    db_city = await crud.delete_city_by_id(db=db, city_id=city_id)
    
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return None


@router.put("/{city_id}", response_model=schemas.CityRead)
async def update_city_by_id(
    city_id: int,
    city_data: schemas.CityCreate,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    db_city = await crud.get_city_by_id(db=db, city_id=city_id)

    if db_city is not None:
        return await crud.update_city_by_id(db=db, city_id=city_id, city_data=city_data)
    raise HTTPException(status_code=404, detail="City not found")