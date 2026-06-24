from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import crud, schemas
from dependencies import get_db

router = APIRouter(prefix="/cities", tags=["cities"])


@router.post("", response_model=schemas.CityResponse, status_code=status.HTTP_201_CREATED)
def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    existing_city = crud.get_city_by_name(db, city.name)
    if existing_city is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"City '{city.name}' already exists",
        )
    return crud.create_city(db, city)


@router.get("", response_model=list[schemas.CityResponse])
def read_cities(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_cities(db, skip=skip, limit=limit)


@router.get("/{city_id}", response_model=schemas.CityResponse)
def read_city(city_id: int, db: Session = Depends(get_db)):
    db_city = crud.get_city(db, city_id)
    if db_city is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"City з id={city_id} not found",
        )
    return db_city


@router.put("/{city_id}", response_model=schemas.CityResponse)
def update_city(
    city_id: int, city_update: schemas.CityUpdate, db: Session = Depends(get_db)
):
    db_city = crud.update_city(db, city_id, city_update)
    if db_city is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"City з id={city_id} not found",
        )
    return db_city


@router.delete("/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_city(city_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_city(db, city_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"City з id={city_id} not found",
        )
