from typing import Annotated, Sequence

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from cities import schemas, crud
from cities.models import City
from dependencies import get_session

router = APIRouter()

SessionDep = Annotated[AsyncSession, Depends(get_session)]


@router.post(
    "/cities",
    response_model=schemas.City,
    tags=["cities"],
    summary="Add a new city"
)
async def create_city(
        city: schemas.CityCreate, db: SessionDep
):
    return await crud.create_city(db=db, city=city)


@router.get(
    "/cities",
    response_model=list[schemas.City],
    tags=["cities"],
    summary="Get all cities"
)
async def get_cities(db: SessionDep):
    return await crud.get_cities(db=db)


@router.get(
    "/cities/{city_id}",
    response_model=schemas.City,
    tags=["cities"],
    summary="Get specific city"
)
async def get_city(city_id: int, db: SessionDep):
    city = await crud.get_city_by_id(db=db, city_id=city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    return city


@router.patch(
    "/cities/{city_id}",
    response_model=schemas.City,
    tags=["cities"],
    summary="Update specific city"
)
async def update_city(
        city_id: int, data: schemas.CityUpdate, db: SessionDep
):
    city = await crud.update_city(db=db, data=data, city_id=city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    return city


@router.delete(
    "/cities/{city_id}",
    tags=["cities"],
    summary="Delete specific city",
    status_code=204
)
async def delete_city(city_id: int, db: SessionDep):
    city = await crud.delete_city(db=db, city_id=city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
