from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from temperature import schemas, crud

router = APIRouter()


@router.get("/temperatures/", response_model=list[schemas.Temperature])
async def read_all_temperatures(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_temperatures(db=db)


@router.get(
    "/temperature/?city_id={city_id}", response_model=list[schemas.Temperature]
)
async def read_temperatures_for_city(city_id: int):
    temperatures = await crud.get_temperatures_by_city_id(city_id=city_id)
    if not temperatures:
        raise HTTPException(
            status_code=404, detail="No temperatures found for this city!"
        )
    return temperatures


@router.post("/temperatures/update", response_model=list[schemas.Temperature])
async def update_temperatures(db: AsyncSession = Depends(get_db)):
    return await crud.update_temperatures_for_all_cities(db=db)
