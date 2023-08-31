from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from . import crud, schemas

router = APIRouter()


@router.get("/temperatures/", response_model=list[schemas.Temperature])
async def get_cities(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_temperatures(db=db)


# @router.get("/temperatures/update/", response_model=list[schemas.Temperature])
# async def get_cities(db: AsyncSession = Depends(get_db)):
#     return await crud.get_all_temperatures(db=db)
