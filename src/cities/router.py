from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies import get_db


from . import schemas, crud

router = APIRouter()


async def validate_city_exists(db: AsyncSession, city_id: int):
    city = await crud.get_city_by_id(db=db, city_id=city_id)
    if not city:
        raise HTTPException(status_code=404, detail=f"City with ID={city_id} not found.")
    return city

@router.post("/cities/", response_model=schemas.City)
async def create_city(
    city: schemas.CityNew,
    db: AsyncSession = Depends(get_db),
):
    exists_city = await crud.get_city_by_name(db=db, name=city.name)
    if exists_city:
        raise HTTPException(
            status_code=400, 
            detail=f"City '{city.name}' already exists. Choose another city."
        )
    new_city = await crud.create_new_city(db=db, city=city)
    return new_city


@router.get("/cities/", response_model=list[schemas.City])
async def read_cities(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_cities(db=db)


@router.get("/cities/{city_id}/", response_model=schemas.City)
async def get_city(
    city_id: int,
    db: AsyncSession = Depends(get_db), 
):
    return await validate_city_exists(db=db, city_id=city_id)


@router.delete("/cities/{city_id}/", status_code=204)
async def delete_city(
    city_id: int,
    db: AsyncSession = Depends(get_db), 
):
    city = await validate_city_exists(db=db, city_id=city_id)
    await crud.delete_city_by_id(db=db, city_id=city_id)
    return Response(status_code=204)


@router.put("/cities/{city_id}/", response_model=schemas.City)
async def update_city(
    city_id: int,
    update_data: schemas.CityNew,
    db: AsyncSession = Depends(get_db), 
):
    city = await validate_city_exists(db=db, city_id=city_id)
    return await crud.update_city_by_id(
        db=db, city_id=city_id, update_data=update_data
    )
