from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from dependencies import get_db
from . import crud, schemas

router = APIRouter()


@router.get("/temperatures/", response_model=list[schemas.Temperature])
async def read_temperatures(
        city_id: int | None = None,
        db: AsyncSession = Depends(get_db)
):
    return await crud.get_temperatures(db=db, city_id=city_id)


@router.post("/temperatures/update")
async def update_temperatures(db: AsyncSession = Depends(get_db)):
    return await crud.update_temperatures(db=db)
