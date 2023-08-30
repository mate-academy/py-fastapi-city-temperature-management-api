from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from city import schemas, crud
from dependencies import get_db

router = APIRouter()


@router.get(
    "/cities/",
    response_model=list[schemas.City]
)
async def read_cities(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_cities(db=db)


@router.get(
    "/cities/{city-id}/",
    response_model=schemas.City
)
async def read_single_city(city_id: int, db: AsyncSession = Depends(get_db)):
    db_city = await crud.get_city(db=db, city_id=city_id)

    if db_city is None:
        raise HTTPException(
            status_code=400,
            detail="city not found"
        )

    return db_city


@router.post(
    "/cities/",
    response_model=schemas.City
)
async def create_city(
        city: schemas.CityCreate,
        db: AsyncSession = Depends(get_db)
):
    return await crud.create_city(db=db, city=city)


@router.put(
    "/cities/{city-id}",
    response_model=schemas.City
)
async def update_city(
        city_id: int,
        city: schemas.CityUpdate,
        db: AsyncSession = Depends(get_db)
):
    db_city = crud.get_city(db=db, city_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return await crud.update_city(db=db, db_city=db_city, city=city)


@router.delete(
    "/cities/{city-id}",
    response_model=schemas.City
)
async def delete_city(
        city_id: int,
        db: AsyncSession = Depends(get_db)
):
    db_city = crud.get_city(db=db, city_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return await crud.delete_city(db=db, db_city=db_city)
