from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from city import schemas, crud
from dependencies import get_db

router = APIRouter()


@router.post("/cities/", response_model=schemas.City)
async def create_note(
    city: schemas.CityCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return await crud.create_city(db=db, city=city)


@router.get("/cities/", response_model=list[schemas.City])
async def read_cities(db: Annotated[AsyncSession, Depends(get_db)]):
    return await crud.get_cities(db=db)


@router.get("/cities/{city_id}", response_model=schemas.City)
async def read_city(
    city_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    city = await crud.get_city_by_id(db=db, city_id=city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@router.put("/cities/{city_id}", response_model=schemas.City)
async def update_city(
    city_id: int,
    city: schemas.CityUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    updated_city = await crud.update_city(
        db=db, city_id=city_id, city_data=city
    )
    if not updated_city:
        raise HTTPException(status_code=404, detail="City not found")

    return updated_city


@router.delete("/cities/{city_id}", status_code=204)
async def delete_city(
    city_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    deleted = await crud.delete_city(db=db, city_id=city_id)
    if not deleted:
        raise HTTPException(
            status_code=404, detail="City not found"
        )
