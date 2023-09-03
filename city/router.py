from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db, common_parameters
from . import crud, schemas

router = APIRouter()


@router.get("/cities/", response_model=list[schemas.CityBase])
async def read_cities(
        commons: Annotated[dict, Depends(common_parameters)],
        db: AsyncSession = Depends(get_db)
) -> list[schemas.CityBase]:
    return await crud.get_all_cities(db=db, **commons)


@router.get("/cities/{city_id}/", response_model=schemas.City)
async def read_city(
        city_id: int, db: AsyncSession = Depends(get_db)
) -> schemas.City:
    result = await crud.get_city_by_id(db=db, city_id=city_id)
    if result is None:
        raise HTTPException(status_code=404, detail="City not found")
    return result


@router.post("/cities/", response_model=schemas.CityBase)
async def create_city(
        city: schemas.CityCreate, db: AsyncSession = Depends(get_db)
) -> dict[schemas.CityBase]:
    db_city = await crud.get_city_by_name(db=db, city_name=city.name)
    if db_city:
        raise HTTPException(
            status_code=400,
            detail="City with this name already exists"
        )

    result = await crud.create_city(city=city, db=db)
    return result


@router.put("/cities/{city_id}/update/", response_model=schemas.CityBase)
async def update_city(
        city_id: int, data: schemas.CityBase, db: AsyncSession = Depends(get_db)
) -> dict[schemas.CityBase]:
    result = await crud.update_city(city_id=city_id, city=data, db=db)
    return result


@router.delete("/cities/{city_id}")
async def delete_city(
        city_id: int, db: AsyncSession = Depends(get_db)
):
    await crud.delete_city(city_id=city_id, db=db)
    return "city deleted"
