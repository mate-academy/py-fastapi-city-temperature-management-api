from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from cities import crud, schemas

router = APIRouter(
    prefix="/cities",
    tags=["Cities"],
)


@router.post("/", response_model=schemas.CityList)
async def create_city(
        city: schemas.CityCreate,
        db: AsyncSession = Depends(get_db),
):
    return await crud.create_city(db, city)


@router.get("/", response_model=list[schemas.CityList])
async def read_cities(
        db: AsyncSession = Depends(get_db),
):
    return await crud.get_all_cities(db)


@router.get("/{city_id}", response_model=schemas.CityList)
async def read_city(
        city_id: int,
        db: AsyncSession = Depends(get_db),
):
    city = await crud.get_city_by_id(db, city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@router.put("/{city_id}", response_model=schemas.CityList)
async def update_city(
        city_id: int,
        city: schemas.CityUpdate,
        db: AsyncSession = Depends(get_db),
):
    db_city = await crud.get_city_by_id(db, city_id)
    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")

    return await crud.update_city(db, db_city, city)


@router.patch("/{city_id}", response_model=schemas.CityList)
async def patch_city(
        city_id: int,
        city: schemas.CityUpdate,
        db: AsyncSession = Depends(get_db),
):
    db_city = await crud.get_city_by_id(db, city_id)
    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")

    return await crud.update_city(db, db_city, city)


@router.delete("/{city_id}", status_code=204)
async def delete_city(
        city_id: int,
        db: AsyncSession = Depends(get_db),
):
    db_city = await crud.get_city_by_id(db, city_id)
    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")

    await crud.delete_city(db, db_city)
