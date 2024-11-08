from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.city import schemas
from src.city import crud
from src.dependencies import get_db

router = APIRouter()


@router.get("/cities/", response_model=list[schemas.City])
async def read_cities(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_cities(db)


@router.post("/cities/", response_model=schemas.City)
async def create_city(city: schemas.CreateCity, db: AsyncSession = Depends(get_db)):
    db_city = await crud.get_city_by_name(db, city.name)
    if db_city:
        raise HTTPException(
            status_code=400,
            detail=f"Such city with name '{db_city.name}' already exists."
        )
    return await crud.create_city(db, city)
