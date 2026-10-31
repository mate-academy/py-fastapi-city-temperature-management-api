from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from city import schemas, crud

router = APIRouter(prefix="/cities", tags=["cities"])

DbSession = Annotated[AsyncSession, Depends(get_db)]


@router.post("/", response_model=schemas.City, status_code=status.HTTP_201_CREATED)
async def city_create(data: schemas.CityCreate, db: DbSession):
    return await crud.create_city(db=db, data=data)


@router.get("/", response_model=list[schemas.City])
async def cities_get(db: DbSession):
    return await crud.get_all_cities(db=db)


@router.get("/{city_id}", response_model=schemas.City)
async def city_get_by_id(city_id: int, db: DbSession):
    city = await crud.get_city_by_id(db=db, city_id=city_id)
    if city is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="City not found"
        )
    return city


@router.put("/{city_id}", response_model=schemas.City)
async def city_update(city_id: int, db: DbSession, data: schemas.CityUpdate):
    city = await crud.update_city(db=db, city_id=city_id, data=data)
    if city is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="City not found"
        )
    return city


@router.delete("/{city_id}", response_model=schemas.City)
async def city_delete(city_id: int, db: DbSession):
    if not await crud.delete_city(db=db, city_id=city_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="City not found"
        )
