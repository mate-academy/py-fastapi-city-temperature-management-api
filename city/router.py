from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from city import schemas, crud
from dependencies import get_db

router = APIRouter()


@router.get("/cities/", response_model=list[schemas.City])
async def read_all_cities(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_cities(db)


@router.get("/cities/{city_id}/", response_model=schemas.City)
async def read_city(city_id: int, db: AsyncSession = Depends(get_db)):
    city = await crud.get_city_by_id(db, city_id)

    if city is None:
        raise HTTPException(status_code=404, detail="City with this ID does not exists")

    return city


@router.post("/cities/", response_model=schemas.City)
async def create_city(city: schemas.CityCreate, db: AsyncSession = Depends(get_db)):
    db_city = await crud.get_city_by_name(db, city.name)

    if db_city:
        raise HTTPException(
            status_code=400, detail="City with this name already exists"
        )

    return await crud.create_city(db, city)


@router.put("/cities/{city_id}/", response_model=schemas.City)
async def update_city(
    new_info: schemas.CityCreate, city_id: int, db: AsyncSession = Depends(get_db)
):
    db_city = await crud.get_city_by_id(db, city_id)

    if db_city is None:
        raise HTTPException(status_code=404, detail="City with this ID does not exists")

    return await crud.update_city_by_id(db, new_info, city_id)


@router.delete("/cities/{city_id}/", response_model=schemas.City)
async def remove_city(city_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.delete_city_by_id(db, city_id)
