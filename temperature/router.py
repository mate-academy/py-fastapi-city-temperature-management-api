from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from temperature import schemas, utils, crud as temperature_crud

router = APIRouter()


@router.get("/temperatures/", response_model=list[schemas.Temperature])
async def read_all_temperatures(
    db: AsyncSession = Depends(get_db),
        city_id: int = None,
        skip: int = 0,
        limit: int = 10,
):
    return await temperature_crud.get_temperatures(
        db=db,
        city_id=city_id,
        skip=skip,
        limit=limit
    )


@router.post("/temperatures/update/", response_model=None)
async def update_temperatures(db: AsyncSession = Depends(get_db)):

    return await utils.update_temperatures(db=db)
