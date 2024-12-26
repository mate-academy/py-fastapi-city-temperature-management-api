from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from . import schemas, crud, models
from dependencies import get_db

router = APIRouter()


@router.get("/temperatures", response_model=list[schemas.Temperature])
async def get_all_temperatures_records(
        db: AsyncSession = Depends(get_db),
) -> list[models.DBTemperature]:
    return await crud.get_all_temperatures_records(db=db)


@router.get(
    "/temperatures/{city_id}",
    response_model=list[schemas.Temperature]
)
async def get_all_temperatures_records_by_city_id(
        city_id: int,
        db: AsyncSession = Depends(get_db)
) -> [models.DBTemperature]:
    return await crud.get_all_temperatures_records_by_city_id(
        city_id=city_id,
        db=db,
    )


@router.post("/temperatures/update", status_code=204)
async def update_temperatures(db: AsyncSession = Depends(get_db)) -> None:
    await crud.update_temperatures(db=db)
