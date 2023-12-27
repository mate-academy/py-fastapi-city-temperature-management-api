from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from . import schemas, crud

router = APIRouter()


@router.get("/cities/", response_model=list[schemas.CityBase])
async def get_cities(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_cities(db=db)


@router.get("/cities/{city_id}/", response_model=schemas.CityBase)
async def get_city_by_id(city_id: int, db: AsyncSession = Depends(get_db)):
    db_city = await crud.get_city_by_id(db=db, city_id=city_id)

    if db_city is None:
        return HTTPException(status_code=404, detail="City not found")

    return db_city


@router.post("/cities/", response_model=schemas.City)
async def create_city(city: schemas.CityCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_city(db=db, city=city)


@router.put("/cities/{city_id}/", response_model=schemas.CityUpdate)
async def update_city(
        city_id: int,
        city: schemas.CityUpdate,
        db: AsyncSession = Depends(get_db),
):
    updated_city = await crud.update_city(
        db=db,
        city_id=city_id,
        city=city.model_dump()
    )

    if updated_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return updated_city


@router.delete("/cities/{city_id}/")
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.delete_city(db=db, city_id=city_id)
