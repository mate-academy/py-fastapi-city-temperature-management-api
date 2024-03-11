from fastapi import (
    APIRouter,
    HTTPException,
    status,
    Depends
)
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from dependencies import get_db
from . import crud, schemas


router = APIRouter()
async_session = Annotated[AsyncSession, Depends(get_db)]


@router.get("/cities/", response_model=list[schemas.City])
async def all_cities(db: async_session):
    return await crud.get_all_cities(db=db)


@router.post("/cities/", response_model=schemas.City)
async def create_city(city: schemas.CreateCity, db: async_session):
    return await crud.create_city(db=db, city=city)


@router.get("/cities/{city_id}/", response_model=schemas.City)
async def get_city(db: async_session, city_id: int):
    city = await crud.get_city(db=db, city_id=city_id)

    if city:
        return city
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="There is no city like that"
    )


@router.patch("/cities/{city_id}/", response_model=schemas.City)
async def update_city(db: async_session, city: schemas.UpdateCity):
    city = await crud.update_city(db=db, city=city)

    if city:
        return city
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="There is no city like that"
    )


@router.delete("/cities/{city_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_city(db: async_session, city_id: int):
    city = await crud.delete_city(db=db, city_id=city_id)

    if not city:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is no city like that"
        )
