from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from dependencies import get_db
from settings import settings
from temperature.crud import get_all_temperatures, update_temperatures
from temperature.schemas import Temperature


router = APIRouter(
    prefix="/temperatures",
    tags=["temperatures"],
)


@router.post("/update", response_model=dict)
async def update_temperature(
    db: AsyncSession = Depends(get_db),
    api_key: str = settings.WEATHER_API_KEY,
):
    result = await update_temperatures(db, api_key)

    return JSONResponse(content={"message": result})


@router.get("/", response_model=list[Temperature])
async def read_all_temperatures_or_temperatures_by_city_id(
        db: AsyncSession = Depends(get_db),
        city_id: int | None = None
):
    return await get_all_temperatures(db=db, city_id=city_id)
