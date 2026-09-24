from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from city import schemas, crud
from dependencies import get_db

router = APIRouter()


@router.post("/cities/", response_model=schemas.City, status_code=status.HTTP_201_CREATED)
async def create_city(city: schemas.CityCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_city(db, city=city)

@router.get("/cities/", response_model=list[schemas.City])
async def get_cities(db: Annotated[AsyncSession, Depends(get_db)]):
    return await crud.get_city_list(db=db)

@router.get("/cities/{city_id}", response_model=schemas.City)
async def get_city_by_id(city_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    return await crud.get_city_by_id(db=db, city_id=city_id)

@router.put("/cities/{city_id}", response_model=schemas.City)
async def update_city_by_id(city_id: int, city_data: schemas.CityUpdate, db: Annotated[AsyncSession, Depends(get_db)]):
    try:
        city = await crud.update_city_by_id(db=db, city_id=city_id, city_data=city_data)

    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="City already exists")

    if city is None:
        raise HTTPException(status_code=400, detail="City does not exist")
    return city

@router.delete("/cities/{city_id}", response_model=schemas.City)
async def delete_city_by_id(city_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    try:
        await crud.delete_city_by_id(db=db, city_id=city_id)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="City does not exist")
