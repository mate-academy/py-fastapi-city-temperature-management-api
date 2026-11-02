from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from cities import schemas, crud
from dependencies import get_db

router = APIRouter(prefix="/cities", tags=["cities"])

@router.get("/", response_model=list[schemas.City])
async def get_cities(db: Annotated[AsyncSession, Depends(get_db)]):
    return await crud.get_all_cities(db=db)

@router.post("/", response_model=schemas.City)
async def create_city(
    city: schemas.CityCreate,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    db_city = await crud.get_city_by_name(db=db, name=city.name)
    if db_city:
        raise HTTPException(
            status_code=400, detail="City with this name already exists"
        )

    return await crud.create_city(
        db=db,
        city=city
    )

@router.delete("/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_city(city_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    return await crud.delete_city(db=db, city_id=city_id)