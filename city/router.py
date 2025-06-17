from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from . import schemas, crud


router = APIRouter(
    prefix="/cities",
    tags=["cities"]
)


@router.get(
    "/",
    response_model=list[schemas.City],
    include_in_schema=True,
    summary="Get cities list",
    tags=["cities"]
)
async def list_cities(db: AsyncSession = Depends(get_db)):
    return await crud.get_cities(db=db)


@router.get(
    "/{city_id}",
    response_model=schemas.City,
    include_in_schema=True,
    summary="Get city details",
    tags=["cities"]
)
async def read_city(city_id: int, db: AsyncSession = Depends(get_db)):
    city = await crud.get_city(db, city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@router.post(
    "/",
    response_model=schemas.City,
    include_in_schema=True,
    summary="Create a new city",
    tags=["cities"]
)
async def create_city(
    city: schemas.CityCreate,
    db: AsyncSession = Depends(get_db),
):
    db_city = await crud.get_city_by_name(db=db, name=city.name)

    if db_city:
        raise HTTPException(
            status_code=400, detail="Such name for City already exists"
        )

    return await crud.create_city(db=db, city=city)


@router.put(
    "/{city_id}",
    include_in_schema=True,
    response_model=schemas.City,
    summary="Update city details",
    tags=["cities"]
)
async def update_city(
    city_id: int,
    city_data: schemas.CityUpdate,
    db: AsyncSession = Depends(get_db),
):
    existing_city = await crud.get_city(db, city_id)
    if not existing_city:
        raise HTTPException(status_code=404, detail="City not found")

    if city_data.name != existing_city.name:
        city_with_same_name = await crud.get_city_by_name(db, city_data.name)
        if city_with_same_name:
            raise HTTPException(
                status_code=400, detail="City with this name already exists"
            )

    updated_city = await crud.update_city(db, city_id, city_data)
    return updated_city


@router.delete(
    "/{city_id}",
    include_in_schema=True,
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete city details",
    tags=["cities"]
)
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)):
    success = await crud.delete_city(db, city_id)
    if not success:
        raise HTTPException(status_code=404, detail="City not found")
    return None
