from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from . import crud, schemas


router = APIRouter()


@router.get("/cities/", response_model=list[schemas.City])
async def read_cities(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_cities(db=db)


@router.post("/cities/", response_model=schemas.City)
async def create_city(
    city: schemas.CityCreate,
    db: AsyncSession = Depends(get_db),
):
    return await crud.create_city(db=db, city=city)


@router.delete("/cities/{city_id}", response_model=schemas.City)
async def delete_city(
    city_id: int,
    db: AsyncSession = Depends(get_db),
):
    city = await crud.delete_city(db=db, city_id=city_id)

    if city is None:
        raise HTTPException(status_code=404, detail="City doesn't exist")
    return city
