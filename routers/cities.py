from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import crud
import schemas
from database import get_db

router = APIRouter(prefix="/cities", tags=["Cities"])

@router.post(
    "",
    response_model=schemas.CityRead,
    status_code=status.HTTP_201_CREATED,
)
def create_city(
    city: schemas.CityCreate,
    db: Session = Depends(get_db),
):
    db_city = crud.create_city(db=db, city=city)
    if db_city is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="City already exists",
        )
    return db_city


@router.get(
    "",
    response_model=List[schemas.CityRead]
)
def get_cities(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return crud.get_cities(db=db, skip=skip, limit=limit)


@router.get(
    "/{city_id}",
    response_model=schemas.CityRead
)
def get_city(
    city_id: int,
    db: Session = Depends(get_db)
):
    city = crud.get_city_by_id(db=db, city_id=city_id)
    if city is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found"
        )
    return city


@router.delete(
    "/{city_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_city(
    city_id: int,
    db: Session = Depends(get_db)
):
    city = crud.delete_city(db=db, city_id=city_id)
    if city is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found"
        )
    return None
