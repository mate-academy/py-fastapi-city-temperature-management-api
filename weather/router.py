from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from dependencies import get_db
from weather import schemas, crud


router = APIRouter()


@router.get("/cities/", response_model=list[schemas.City])
async def read_all_cities(db: Session = Depends(get_db)):
    return await crud.get_all_cities(db=db)


@router.get("/cities/{city_id}/", response_model=schemas.City)
async def read_city(city_id: int, db: Session = Depends(get_db)):
    db_city = await crud.get_city_by_id(db=db, city_id=city_id)
    return db_city


@router.post("/cities/", response_model=schemas.City)
async def create_city(
        city: schemas.CityCreate,
        db: Session = Depends(get_db)
):
    return await crud.create_city(db=db, city=city)


@router.put("/cities/{city_id}/", response_model=schemas.City)
async def update_city(
        city_id: int,
        city: schemas.CityUpdate,
        db: Session = Depends(get_db)
):
    return await crud.update_city_by_city_id(
            db=db,
            city_id=city_id,
            city_data=city,
        )


@router.delete("/cities/{city_id}/",)
async def delete_city(city_id: int, db: Session = Depends(get_db)):
    return await crud.delete_city(db=db, city_id=city_id)

