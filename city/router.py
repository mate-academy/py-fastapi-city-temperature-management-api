from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from typing import List

from city import crud
from dependencies import get_db
from city import schemas

router = APIRouter()


@router.get("/cities/", response_model=List[schemas.CityList])
def get_all_cities(db: Session = Depends(get_db)) -> schemas.CityList:
    return crud.get_all_cities(db)


@router.post("/cities/", response_model=schemas.CityList)
def create_city(
        city: schemas.CityCreate,
        db: Session = Depends(get_db)
) -> schemas.CityList:
    return crud.create_city(db=db, city=city)


@router.get("/cities/{city_id}/", response_model=schemas.CityList)
def get_city_by_id(
        city_id: int,
        db: Session = Depends(get_db)
) -> schemas.CityList:
    db_city = crud.get_city_by_id(db=db, city_id=city_id)
    if db_city:
        return db_city

    raise HTTPException(status_code=404, detail="City not found")


@router.put("/cities/{city_id}/", response_model=schemas.CityList)
def update_city(
        city_id: int,
        city: schemas.CityCreate,
        db: Session = Depends(get_db)
) -> schemas.CityList:
    db_city = crud.update_city(city_id=city_id, city=city, db=db)
    if db_city:
        return db_city

    raise HTTPException(status_code=404, detail="City not found")


@router.delete("/cities/{city_id}/", response_model=dict)
def delete_city(
        city_id: int,
        db: Session = Depends(get_db)
) -> schemas.CityList:
    success = crud.delete_city(db=db, city_id=city_id)
    if success:
        return {"detail": "City deleted successfully"}
    raise HTTPException(status_code=404, detail="City not found")
