from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from main import get_db
from fastapi import APIRouter

router = APIRouter(prefix="/cities", tags=["Cities"])

@router.get("/cities/", response_model=list[schemas.City])
async def read_cities(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100
):
    return await crud.get_all_cities(db, skip=skip, limit=limit)

@router.post("/cities/", response_model=schemas.City)
async def create_city(
        city: schemas.CityCreate,
        db: Session = Depends(get_db),
):
    db_city = await crud.get_city_by_name(db, name=city.name)

    if db_city:
        raise HTTPException(
            status_code=409, detail="City with this name already exists"
        )

    return await crud.create_city(db, city=city)

@router.get("/cities/{city_id}", response_model=schemas.City)
async def read_city(city_id: int, db: Session = Depends(get_db)):

    city = await crud.get_city_by_id(db, city_id=city_id)

    if city is None:
        raise HTTPException(
            status_code=404,
            detail="City with this id does not exist"
        )
    return city

@router.put("/cities/{city_id}", response_model=schemas.City)
async def update_city(
    city_id: int,
    city: schemas.CityCreate,
    db: Session = Depends(get_db),
):
    db_city = await crud.get_city_by_id(db, city_id)

    if db_city is None:
        raise HTTPException(
            status_code=404,
            detail="City with this id does not exist"
        )

    return await crud.update_city(db, city_id, city)

@router.delete("/cities/{city_id}")
async def delete_city(
        city_id: int,
        db: Session = Depends(get_db),
):
    city = await crud.get_city_by_id(db, city_id=city_id)

    if city is None:
        raise HTTPException(
            status_code=404,
            detail="City with this id does not exist"
        )
    return await crud.delete_city(db, city_id=city_id)
