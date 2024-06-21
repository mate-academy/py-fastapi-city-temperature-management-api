from fastapi import APIRouter, Depends, HTTPException
from h11 import Response
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from . import schemas, crud

router = APIRouter()


@router.get("/cities/", response_model=list[schemas.City])
async def read_cities(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_cities(db=db)


@router.post("/cities/", response_model=schemas.City)
async def create_city(
        city: schemas.CityCreate,
        db: AsyncSession = Depends(get_db),
):
    db_city = await crud.get_city_by_name(db=db, name=city.name)

    if db_city:
        raise HTTPException(
            status_code=400, detail="City already exists"
        )

    created_city = await crud.create_city(db=db, city=city)
    return created_city if created_city else Response(status_code=204)


@router.delete("/cities/{city_id}/", response_model=schemas.City)
async def delete_city(
        city_id: int,
        db: AsyncSession = Depends(get_db)):
    deleted_city = await crud.delete_city(db=db, city_id=city_id)
    return deleted_city if deleted_city else Response(status_code=204)
