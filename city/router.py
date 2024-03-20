from fastapi import (
    APIRouter,
    status,
    Depends
)
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from project_engine.dependencies import get_db
from .utils import ensure_city_exist
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
@ensure_city_exist
async def get_city(db: async_session, city_id: int):
    return await crud.get_city(db=db, city_id=city_id)


@router.patch("/cities/{city_id}/", response_model=schemas.City)
@ensure_city_exist
async def update_city(
        city_id: int, db: async_session, city: schemas.UpdateCity
):
    return await crud.update_city(db=db, city=city, city_id=city_id)


@router.delete("/cities/{city_id}/", status_code=status.HTTP_204_NO_CONTENT)
@ensure_city_exist
async def delete_city(db: async_session, city_id: int):
    return await crud.delete_city(db=db, city_id=city_id)
