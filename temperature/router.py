from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from temperature import schemas, crud

router = APIRouter()


@router.get("/temperatures/", response_model=list[schemas.Temperature])
async def get_temperatures(
        skip: int = 0,
        limit: int = 5,
        db: AsyncSession = Depends(get_db),
        city_id: int = None
):
    return await crud.get_all_temperatures(
        db=db,
        city_id=city_id,
        skip=skip,
        limit=limit
    )


@router.post("/temperatures/update/", response_model=list[schemas.Temperature])
async def update_temperatures(db: AsyncSession = Depends(get_db)):
    await crud.update_temperature(db)
    return await crud.get_all_temperatures(db=db)
