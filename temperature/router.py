from fastapi import APIRouter, Depends
from fastapi_pagination import add_pagination
from sqlalchemy.ext.asyncio import AsyncSession

from temperature import schemas, crud
import dependecies

router = APIRouter()
add_pagination(router)


@router.get("/", response_model=list[schemas.Temperature])
async def get_temperatures(
        db: AsyncSession = Depends(dependecies.get_db)
) -> list:
    return await crud.get_temperatures(db=db)


@router.post("/update/")
async def update_temperatures(
        db: AsyncSession = Depends(dependecies.get_db)
) -> dict:
    await crud.update_city_temperature(db=db)
    return {"message": "Temperatures updated"}
