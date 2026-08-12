from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from temperature import schemas, crud
from temperature.weather_service import update_temperatures

router = APIRouter()


@router.get(
    "/temperatures/",
    response_model=list[schemas.Temperature],
)
async def read_temperatures(
    db: Annotated[AsyncSession, Depends(get_db)],
    city_id: int | None = None,
):
    return await crud.get_all_temperatures(
        db=db,
        city_id=city_id,
    )


@router.post("/temperatures/update")
async def update_temp(db: Annotated[AsyncSession, Depends(get_db)]):
    await update_temperatures(db)
    return {"detail": "Temperatures updated"}
