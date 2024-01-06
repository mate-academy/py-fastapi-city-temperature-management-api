import asyncio

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from . import schemas, crud, utils


router = APIRouter()


@router.get("/temperatures/", response_model=list[schemas.Temperature])
async def read_temperatures(
        db: AsyncSession = Depends(get_db)
) -> list[schemas.Temperature]:
    return await crud.get_all_temperatures(db=db)


@router.get("/temperatures/{city_id}/", response_model=schemas.Temperature)
async def read_temperature_for_city(
        city_id: int, db: AsyncSession = Depends(get_db)
) -> schemas.Temperature:
    return await crud.get_temperature_for_city(db=db, city_id=city_id)


@router.post("/temperatures/update", response_model=dict)
def update_temperatures(
        db: AsyncSession = Depends(get_db)
) -> dict:
    asyncio.run(utils.gather_temperatures(db))
    return {"status_code": 204, "message": "Temperatures Updated!"}
