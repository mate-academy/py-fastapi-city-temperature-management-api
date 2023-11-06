from fastapi import Depends, HTTPException, Response, status
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from cities import schemas, crud

from dependencies import get_db


router = APIRouter()


@router.get("/cities/", response_model=list[schemas.City])
async def get_cities(db: AsyncSession = Depends(get_db)):
    return await crud.read_cities(db=db)


@router.post("/cities/", response_model=schemas.City)
async def create_city(
    city: schemas.CityCreate, db: AsyncSession = Depends(get_db)
):
    return await crud.create_city(city=city, db=db)


@router.get("/cities/{city_id}/", response_model=schemas.CityDetail)
async def get_city(city_id: int, db: AsyncSession = Depends(get_db)):
    db_city = await crud.read_city(city_id=city_id, db=db)
    if db_city is None:
        raise HTTPException(
            status_code=404, detail=f"There is no city with id {city_id}"
        )
    return db_city


@router.put("/cities/{city_id}/", response_model=schemas.City)
async def update_city(
    city_id: int, city: schemas.CityUpdate, db: AsyncSession = Depends(get_db)
):
    db_city = await crud.update_city(city_id=city_id, city=city, db=db)
    if db_city is None:
        raise HTTPException(
            status_code=404, detail=f"There is no city with id {city_id}"
        )
    return db_city


@router.delete("/cities/{city_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)):
    if not await crud.delete_city(city_id=city_id, db=db):
        raise HTTPException(
            status_code=404, detail=f"There is no city with id {city_id}"
        )
    return None
