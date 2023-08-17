from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from city import crud, schemas


router = APIRouter()

CITY_NOT_FOUND = HTTPException(status_code=404, detail="City not found")


#
@router.get("/cities/", response_model=list[schemas.City])
async def read_cities(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_cities(db=db)


@router.get("/cities/{city_id}", response_model=schemas.City)
async def read_single_city(city_id: int, db: AsyncSession = Depends(get_db)):
    city = await crud.get_single_city(db=db, city_id=city_id)
    if city is None:
        raise CITY_NOT_FOUND
    return city


@router.post("/cities/", response_model=schemas.City)
async def create_city(
    city: schemas.CityCreate, db: AsyncSession = Depends(get_db)
):
    return await crud.create_city(db=db, city=city)


@router.put("/cities/{city_id}", response_model=schemas.City)
async def update_city(
    city_id: int, city: schemas.CityCreate, db: AsyncSession = Depends(get_db)
):
    return await crud.update_city(db=db, city_id=city_id, city=city)


@router.delete("/cities/{city_id}", response_model=schemas.City)
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await delete_city(db=db, city_id=city_id)
    if not deleted:
        raise CITY_NOT_FOUND
    return {"id": city_id}
