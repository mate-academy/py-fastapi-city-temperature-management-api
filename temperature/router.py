from typing import Sequence

from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from models import Temperature
from temperature import crud, schemas


router = APIRouter()


@router.get('/list/', response_model=list[schemas.Temperature])
async def read_temperatures(
        db: AsyncSession = Depends(get_db)
) -> Sequence[Temperature]:
    return await crud.get_list_temperature(db=db)


@router.get('/{city_id}', response_model=schemas.Temperature)
async def read_temperature_of_city(
        city_id: int, db: AsyncSession = Depends(get_db)
) -> Temperature:
    temperature_of_city = await crud.get_temperature_by_city_id(
        db=db, city_id=city_id
    )
    if temperature_of_city is None:
        raise HTTPException(
            status_code=404, detail=f"City with id {city_id} not found"
        )

    return temperature_of_city
