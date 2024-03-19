from fastapi import (
    APIRouter,
    Depends,
    Query
)
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from dependencies import get_db
from . import crud, scraper, schemas


router = APIRouter()
async_session = Annotated[AsyncSession, Depends(get_db)]


@router.get("/temperatures/", response_model=list[schemas.Temperature])
async def get_all_temperatures(db: async_session, city_id: int = Query(0, gt=0)):
    if city_id:
        # filter temperatures for specific city 'city_id'
        return await crud.get_temperatures_by_city_id(db=db, city_id=city_id)
    return await crud.get_all_temperatures(db=db)


@router.post("/temperatures/update/")
async def update_temperatures(db: async_session) -> None:
    """Update Cities Temperature"""
    return await scraper.scrape_temperatures(db=db)
