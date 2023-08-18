from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from dependencies import get_db
from settings import settings
from temperature import crud, schemas


router = APIRouter()


@router.get("/temperatures/", response_model=list[schemas.Temperature])
async def read_temperatures(
    db: AsyncSession = Depends(get_db), city_id: int | None = None
):
    return await crud.get_all_temperatures(db=db, city_id=city_id)


@router.post("/temperatures/update")
async def update_temperature(
    api_key: str = settings.WEATHER_API_KEY,
    db: AsyncSession = Depends(get_db),
):
    result = await crud.update_temperature(db, api_key)
    return JSONResponse(content={"message": result})
