from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from temperature import schemas, crud

router = APIRouter()


@router.post("/temperatures/update/")
async def update_temperature(
        db: AsyncSession = Depends(get_db),
):
    updated = await crud.update_temperatures(db)

    return {
        "message": f"Updated temperature for {updated} cities."
    }


@router.get("/temperatures/", response_model=list[schemas.TemperatureResponse])
async def get_temperatures(
        city_id: int | None = None,
        db: AsyncSession = Depends(get_db),
):
    return await crud.get_temperatures(db, city_id)
