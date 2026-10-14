from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession


from dependencies import get_db
from cities import schemas, crud
from cities.utils import _get_city_or_404

router = APIRouter


@router.post("/cities/", response_model=schemas.CityList)
async def create_city(
        db: Annotated[AsyncSession, Depends(get_db)],
        city: schemas.CityCreate
):
    db_city = await crud.get_city_by_name(db=db, name=city.name)
    if db_city:
        raise HTTPException(
            status_code=400, detail="City with this name already exists"
        )

    return crud.create_city(db=db, city=city)

@router.get("/cities/", response_model=schemas.CityList)
async  def cities_list(
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return await crud.get_cities(db=db)

@router.get("/cities/{id}/", response_model=schemas.CityDetail)
async def city_detail(
    db: Annotated[AsyncSession, Depends(get_db)],
    city_id: int,
):
    city = await _get_city_or_404(db=db, city_id=city_id)

    return city

@router.put("/cities/{id}/", response_model=schemas.CityList)
async def city_update(
    db: Annotated[AsyncSession, Depends(get_db)],
    city_id: int,
    city_data: schemas.CityUpdate
):
    city = await _get_city_or_404(db=db, city_id=city_id)

    return await crud.update_city(db=db, db_city=city, city_data=city_data)


@router.delete("/cities/{city_id}/")
async def city_delete(
    city_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    db_city = await _get_city_or_404(db, city_id)
    await crud.delete_city(db=db, db_city=db_city)
    return {"detail": "City deleted"}

