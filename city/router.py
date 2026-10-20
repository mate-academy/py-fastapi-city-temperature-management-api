from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from city import schemas, crud
from dependencies import get_db

router = APIRouter()

@router.get("/cities/", response_model=list[schemas.City])
async def read_cities(db: Annotated[AsyncSession, Depends(get_db)]):
    return await crud.get_all_cities(db)


@router.post("/cities/", response_model=schemas.CityCreate)
async def create_city(city: schemas.CityCreate, db: Annotated[AsyncSession, Depends(get_db)]):
    return await crud.create_city(db=db, city=city)


@router.delete("/cities/{city_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_city(city_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    return await crud.delete_city(db=db, city_id=city_id)