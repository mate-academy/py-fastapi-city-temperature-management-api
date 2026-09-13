from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import city_schema
from app.services import city_service

from dependencies import get_db

router = APIRouter(tags=["city"])

CommonDB = Annotated[AsyncSession, Depends(get_db)]


@router.get("/cities", response_model=list[city_schema.City])
async def read_cities(db: CommonDB):
    return await city_service.get_all_cities(db=db)


@router.post("/cities", response_model=city_schema.City)
async def create_city(city: city_schema.CityCreate, db: CommonDB):
    db_city = await city_service.get_city_by_name(db=db, name=city.name)

    if db_city:
        raise HTTPException(
            status_code=400, detail="City with this name already exists"
        )

    return await city_service.create_city(db=db, city=city)


@router.get("/cities/{city_id}", response_model=city_schema.City)
async def read_single_city(city_id: int, db: CommonDB):
    db_city = await city_service.get_city_by_id(db=db, city_id=city_id)

    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")

    return db_city


@router.put("/cities/{city_id}", response_model=city_schema.City)
async def update_city(
        city_id: int,
        city: city_schema.CityCreate,
        db: CommonDB
):
    db_city = await city_service.get_city_by_id(db=db, city_id=city_id)

    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")

    city_with_same_name = await city_service.get_city_by_name(
        db=db,
        name=city.name
    )

    if city_with_same_name and city_with_same_name.id != city_id:
        raise HTTPException(
            status_code=400,
            detail="Another city with this name already exists"
        )

    return await city_service.update_city(db=db, city_id=city_id, city=city)


@router.delete("/cities/{city_id}")
async def delete_city(city_id: int, db: CommonDB):
    db_city = await city_service.get_city_by_id(db=db, city_id=city_id)

    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")

    await city_service.delete_city(db=db, city=db_city)

    return {"detail": "City deleted successfully"}
