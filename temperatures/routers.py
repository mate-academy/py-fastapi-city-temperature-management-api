from fastapi import APIRouter, Depends

from temperatures import schemas, crud

from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db

temperature_routers = APIRouter()


@temperature_routers.get("/temperatures/", response_model=list[schemas.TemperatureSchema])
async def read_temperatures(db: AsyncSession = Depends(get_db), city_id: int | None = None):
    return await crud.get_all_temperatures(db=db, city_id=city_id)