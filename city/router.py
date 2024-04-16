from typing import Sequence

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from city import crud, schemas
from dependencies import get_db

router = APIRouter()


@router.get("/cities/", response_model=list[schemas.City])
async def read_cities(db: AsyncSession = Depends(get_db)) -> Sequence[schemas.City]:
    return await crud.get_all_cities(db=db)


@router.get("/cities/{city_id}/", response_model=schemas.City)
async def read_single_city(
    city_id: int, db: AsyncSession = Depends(get_db)
) -> schemas.City:
    if city := await crud.get_city_by_id(db=db, city_id=city_id):
        return city

    raise HTTPException(status_code=404, detail="City not found")


@router.post("/cities/", response_model=schemas.City, status_code=201)
async def create_city(
    city: schemas.CityCreate, db: AsyncSession = Depends(get_db)
) -> schemas.City:
    if await crud.get_city_by_name(db=db, city_name=city.name):
        raise HTTPException(
            status_code=404, detail="City with such name already exists"
        )

    return await crud.create_city(db=db, city=city)


@router.put("/cities/{city_id}/", response_model=schemas.City)
async def update_city(
    city: schemas.CityUpdate, city_id: int, db: AsyncSession = Depends(get_db)
) -> schemas.City:
    if not await crud.get_city_by_id(db=db, city_id=city_id):
        raise HTTPException(status_code=404, detail="City not found")

    if existed_city_by_name := await crud.get_city_by_name(db=db, city_name=city.name):
        if existed_city_by_name.id != city_id:

            raise HTTPException(
                status_code=404, detail="City with such name already exists"
            )

    updated_city = await crud.update_city(db=db, city_id=city_id, city=city)

    return updated_city


@router.delete("/cities/{city_id}/", status_code=204)
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)) -> None:
    if not await crud.get_city_by_id(db=db, city_id=city_id):
        raise HTTPException(status_code=404, detail="City not found")

    await crud.delete_city(db=db, city_id=city_id)
