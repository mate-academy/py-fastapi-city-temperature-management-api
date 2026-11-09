import crud
import schemas
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from db.engine import get_db


router = APIRouter(
    prefix="/cities",
    tags=["Cities"]
)


@router.get("/", response_model=list[schemas.CityResponse])
def get_all_cities(
        skip: int = Query(default=0, ge=0),
        limit: int = Query(default=10, ge=1, le=100),
        database: Session = Depends(get_db)
):
    return crud.get_all_cities(database, skip, limit)


@router.get("/{city_id}/", response_model=schemas.CityResponse)
def get_city_by_id(
        city_id: int,
        database: Session = Depends(get_db)
):
    city = crud.get_city_by_id(database, city_id)

    if city is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found"
        )

    return city


@router.post(
    "/",
    response_model=schemas.CityResponse,
    status_code=status.HTTP_201_CREATED
)
def create_city(
        city: schemas.CityCreate,
        database: Session = Depends(get_db)
):
    return crud.create_city(database, city)


@router.put("/{city_id}/", response_model=schemas.CityResponse)
def update_city(
        city_id: int,
        city: schemas.CityCreate,
        database: Session = Depends(get_db)
):
    updated_city = crud.update_city(database, city_id, city)

    if updated_city is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found"
        )

    return updated_city


@router.delete(
    "/{city_id}/",
    status_code=status.HTTP_204_NO_CONTENT
)

def delete_city(
        city_id: int,
        database: Session = Depends(get_db)
):
    deleted = crud.delete_city(database, city_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found"
        )

    return None
