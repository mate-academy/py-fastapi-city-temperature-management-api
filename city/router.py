from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

import dependencies
from city import crud, schemas

router = APIRouter()


@router.get("/cities/", response_model=list[schemas.CityList])
async def get_city_list(
    db: AsyncSession = Depends(dependencies.get_db)
):
    return await crud.get_all_cities(db=db)


@router.post("/cities/", response_model=schemas.CityList)
async def create_city(
    city: schemas.CityCreate,
    db: AsyncSession = Depends(dependencies.get_db)
):
    return await crud.create_city(db=db, city=city)


@router.delete("/cities/{city_id}")
async def delete_city(
    city_id: int,
    db: AsyncSession = Depends(dependencies.get_db)
):
    return await crud.delete_city(db=db, city_id=city_id)