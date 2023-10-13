from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from city import schemas, crud
from dependencies import get_db

router = APIRouter()


@router.get("/cities/", response_model=list[schemas.City])
async def list_cities(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_cities(db=db)


@router.post("/cities/", response_model=schemas.City)
async def create_city(
    city: schemas.CityCreate, db: AsyncSession = Depends(get_db)
):
    db_city = await crud.get_city_by_name(db=db, name=city.name)
    if db_city:
        raise HTTPException(
            status_code=400, detail="This city is already exist in DB"
        )
    return await crud.create_city(db=db, city=city)


@router.get("/cities/{city_id}", response_model=schemas.City)
async def retrieve_city_by_id(
    city_id: int, db: AsyncSession = Depends(get_db)
):
    db_city = await crud.get_city_by_id(db=db, city_id=city_id)
    if db_city:
        return db_city
    raise HTTPException(status_code=404, detail="City not found")


@router.put("/cities/{city_id}", response_model=schemas.City)
async def update_city_by_id(
    city_id: int,
    updated_city: schemas.CityUpdate,
    db: AsyncSession = Depends(get_db),
):
    db_city = await crud.get_city_by_id(db=db, city_id=city_id)
    if db_city:
        updated_data = await crud.update_city(
            db=db, city_id=city_id, updated_city=updated_city
        )
        return updated_data

    raise HTTPException(status_code=404, detail="City not found")


@router.delete("/cities/{city_id}", response_model=dict)
async def delete_city_by_id(city_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.delete_city(db=db, city_id=city_id)
