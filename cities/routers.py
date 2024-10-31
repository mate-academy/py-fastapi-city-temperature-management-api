from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from cities import schemas, crud
from dependencies import get_db


router = APIRouter()


@router.post("/cities/", response_model=schemas.CityResponse)
async def create_city(
    city: schemas.CityCreate, db: AsyncSession = Depends(get_db)
):
    return await crud.create_city(db=db, city=city)


@router.get("/cities/", response_model=list[schemas.CityResponse])
async def read_cities(db: AsyncSession = Depends(get_db)):
    return await crud.get_cities(db=db)


@router.get("/cities/{city_id}/", response_model=schemas.CityResponse)
async def read_city(city_id: int, db: AsyncSession = Depends(get_db)):
    city = await crud.get_city(db=db, city_id=city_id)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@router.put("/cities/{city_id}/", response_model=schemas.CityResponse)
async def update_city(
    city_id: int, city: schemas.CityCreate, db: AsyncSession = Depends(get_db)
):
    db_city = await crud.update_city(db=db, city_id=city_id, city=city)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city


@router.delete("/cities/{city_id}/", response_model=dict)
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)):
    success = await crud.delete_city(db=db, city_id=city_id)
    if not success:
        raise HTTPException(status_code=404, detail="City not found")
    return {"detail": "City deleted successfully"}
