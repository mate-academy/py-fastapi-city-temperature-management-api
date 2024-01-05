from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from city import crud, schemas
from dependencies import get_db

router = APIRouter()


@router.get("/cities", response_model=list[schemas.City])
async def read_cities(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_cities(db)


@router.post("/cities", response_model=schemas.City)
async def create_city(
        city: schemas.CityCreate,
        db: AsyncSession = Depends(get_db)
):
    db_city = await crud.get_cities_by_name(db=db, name=city.name)
    if db_city:
        raise HTTPException(
            status_code=400,
            detail="City with this name already exists"
        )
    return await crud.create_city(db=db, city=city)


@router.get("/cities/{city_id}/", response_model=schemas.City)
async def get_single_city(city_id: int, db: AsyncSession = Depends(get_db)):
    city = await crud.get_city_by_id(db, city_id)
    if not city:
        raise HTTPException(
            status_code=400,
            detail="City with this id doesn't exist"
        )
    return city


@router.put("/cities/{city_id}/", response_model=schemas.City)
async def update_city(
        city_id: int,
        city: schemas.CityCreate,
        db: AsyncSession = Depends(get_db)
):
    db_city = await crud.get_city_by_id(db=db, city_id=city_id)
    if not db_city:
        raise HTTPException(
            status_code=400,
            detail="City with this id doesn't exist"
        )
    return await crud.update_city(db=db, city_id=city_id, city=city)


@router.delete("/cities/{city_id}/")
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)):
    db_city = await crud.get_city_by_id(db=db, city_id=city_id)
    if not db_city:
        raise HTTPException(
            status_code=400,
            detail="City with this id doesn't exist"
        )
    return await crud.delete_city(db=db, city_id=city_id)
