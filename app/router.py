from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, schemas
from app.dependencies import get_db
from app.models import City
from app.schemas import CityListSchema

router = APIRouter()


@router.get("/cities", response_model=list[CityListSchema])
async def get_cities(db: Annotated[AsyncSession, Depends(get_db)]):
    return await crud.get_all_cities(db=db)


@router.post("/cities", response_model=CityListSchema)
async def create_cities(
        city: schemas.CityCreateSchema,
        db: Annotated[AsyncSession, Depends(get_db)]) -> CityListSchema:
    city_to_check = await db.scalar(select(City).where(City.name == city.name))
    if city_to_check:
        raise HTTPException(status_code=400, detail="City already exists")
    return await crud.create_city(db=db, city=city)


@router.delete("/cities/{id}")
async def delete_cities(
        city_id: int,
        db: Annotated[AsyncSession, Depends(get_db)]
):
    return await crud.delete_city(db=db, city_id=city_id)