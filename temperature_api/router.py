from fastapi import APIRouter, Depends, Query

from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from . import crud
from temperature_api import schemas

router = APIRouter()


@router.get("/temperatures/", response_model=list[schemas.TemperatureSchema])
async def get_temperature(
        city_id: int = None,
        db: AsyncSession = Depends(get_db)
):
    if city_id is not None:
        result = await crud.get_temperature_by_city_id(db=db, city_id=city_id)
        return result
    return await crud.get_temperature_list(db=db)
