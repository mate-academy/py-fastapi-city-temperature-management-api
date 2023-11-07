from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from temperature import schemas, crud as temperature_crud

router = APIRouter()


@router.get("/temperatures/", response_model=list[schemas.Temperature])
async def read_all_temperatures(
    db: AsyncSession = Depends(get_db),
    city_id: int = None,
) -> list[schemas.Temperature]:
    return await temperature_crud.get_temperatures(
        db=db,
        city_id=city_id,
    )


@router.post("/temperatures/update/", response_model=None)
async def update_temperatures(db: AsyncSession = Depends(get_db)) -> dict:
    await temperature_crud.update_temperatures(db=db)
    return {"message": "Temperatures updated for all cities"}
