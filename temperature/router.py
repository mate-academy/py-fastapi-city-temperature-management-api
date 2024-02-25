from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from temperature import crud, schemas

router = APIRouter()


@router.post("/temperatures/update/")
async def update_temperature(db: AsyncSession = Depends(get_db)):
    return await crud.update_temperature(db=db)


@router.get("/temperatures/", response_model=list[schemas.TemperatureList])
async def all_temperatures(db: AsyncSession = Depends(get_db), city_id: int = None):
    return await crud.get_all_temperatures(db=db, city_id=city_id)
