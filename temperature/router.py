from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from temperature import schemas, crud

router = APIRouter()


@router.get("/temperatures/", response_model=list[schemas.Temperature])
async def read_temperatures(db: Annotated[AsyncSession, Depends(get_db)]):
    return await crud.get_all_temperatures(db)


@router.get("/temperatures/{city_id}/", response_model=list[schemas.Temperature])
async def read_temperatures_by_city_id(city_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    return await crud.get_temperatures_by_city_id(db=db, city_id=city_id)