from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from temperature_api import crud, schemas


router = APIRouter()


@router.get("/temperatures/", response_model=list[schemas.Temperature])
async def get_all_temperatures(db: AsyncSession = Depends(get_db)):
    return await crud.get_temperatures(db)


@router.get("/temperatures/{temp_id}", response_model=schemas.Temperature)
async def get_temperature(temp_id: int, db: AsyncSession = Depends(get_db)):
    temp = await crud.get_temperature(db, temp_id)
    if temp is None:
        raise HTTPException(
            status_code=400,
            detail="There is no such temperature"
        )
    return temp


@router.post("/temperatures/update")
async def update_temperatures(db: AsyncSession = Depends(get_db)):
    await crud.update_temperatures(db)
    return {"message": "Temperature data updated"}
