from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from . import crud, schemas

router = APIRouter()


@router.get("/cities/", response_model=list[schemas.City])
async def get_cities(db: AsyncSession = Depends(get_db)):
    return await crud.list_cities(db=db)


@router.get("/cities/{city_id}/", response_model=schemas.City)
async def get_city(city_id: int, db: AsyncSession = Depends(get_db)):
    db_city = await crud.retrieve_city(city_id=city_id, db=db)

    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return db_city


@router.post("/cities/", response_model=schemas.City)
async def create_city(
        city: schemas.CityCreate,
        db: AsyncSession = Depends(get_db)
):
    db_city = await crud.get_city_by_name(db=db, city_name=city.name)

    if db_city:
        raise HTTPException(
            status_code=400, detail="City with such name already exists"
        )

    return await crud.create_city(db=db, city=city)


@router.delete("/cities/{city_id}/")
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)):
    deleted_city = await crud.delete_city(
        db=db,
        city_id=city_id,
    )

    if deleted_city:
        return {"message": "City delete"}
    else:
        raise HTTPException(status_code=404, detail="City not found")


@router.put("/cities/{city_id}/")
async def update_city(
        city_id: int,
        city: dict,
        db: AsyncSession = Depends(get_db)
):
    updated_city = await crud.update_city(
        db=db,
        city_id=city_id,
        city=city,
    )

    if updated_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    else:
        return updated_city
