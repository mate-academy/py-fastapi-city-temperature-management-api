from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from . import crud, schemas

router = APIRouter(prefix="/cities", tags=["Cities"])


@router.post("/", response_model=schemas.CityResponse)
async def create_city(
        city: schemas.CityCreate,
        db: AsyncSession = Depends(get_db)
):
    try:
        return await crud.create_city(db, city)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[schemas.CityResponse])
async def get_all_cities(db: AsyncSession = Depends(get_db)):
    return await crud.get_cities(db)


@router.delete("/{city_id}", response_model=dict)
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)):
    if await crud.delete_city(db, city_id):
        return {"message": "City deleted successfully"}
    raise HTTPException(status_code=404, detail="City not found")
