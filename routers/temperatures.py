from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

import crud
import schemas
from database import get_db
from fastapi import APIRouter

router = APIRouter(
    prefix="/temperatures",
    tags=["Temperatures"],
)


@router.get("/", response_model=list[schemas.Temperature])
async def read_temperatures(
        db: AsyncSession = Depends(get_db),
        skip: int = 0,
        limit: int = 100,
        city_id: int | None = None,
):
    return await crud.get_all_temperature(db, skip=skip, limit=limit, city_id=city_id)

@router.post("/update")
async def update_temperatures(
    db: AsyncSession = Depends(get_db),
):
    await crud.temperature_update(db)
    return {"message": "Temperatures updated"}


def router():
    return None