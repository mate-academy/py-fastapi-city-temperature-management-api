from fastapi import APIRouter, Depends
from fastapi_pagination import add_pagination
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from temperature import schemas, crud
import dependecies

router = APIRouter()
add_pagination(router)


@router.get("/", response_model=list[schemas.Temperature])
async def get_temperatures(db: AsyncSession = Depends(dependecies.get_db)):
    return await crud.get_temperatures(db=db)


@router.post("/update/")
async def update_temperatures(db: AsyncSession = Depends(dependecies.get_db)):
    await crud.update_city_temperature(db=db)
    return {"message": "Temperatures updated"}
