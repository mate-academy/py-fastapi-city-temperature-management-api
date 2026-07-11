from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.dependencies import get_db

router = APIRouter(
    prefix="/cities",
    tags=["Cities"],
)


@router.post("/", response_model=schemas.CityResponse)
def create_city(
    city: schemas.CityCreate,
    db: Session = Depends(get_db),
):
    return crud.create_city(db, city)


@router.get("/", response_model=list[schemas.CityResponse])
def get_cities(
    db: Session = Depends(get_db),
):
    return crud.get_cities(db)


@router.get("/{city_id}", response_model=schemas.CityResponse)
def get_city(
    city_id: int,
    db: Session = Depends(get_db),
):
    city = crud.get_city(db, city_id)

    if city is None:
        raise HTTPException(
            status_code=404,
            detail="City not found",
        )

    return city


@router.put("/{city_id}", response_model=schemas.CityResponse)
def update_city(
    city_id: int,
    city: schemas.CityCreate,
    db: Session = Depends(get_db),
):
    updated_city = crud.update_city(
        db=db,
        city_id=city_id,
        city_data=city,
    )

    if updated_city is None:
        raise HTTPException(
            status_code=404,
            detail="City not found",
        )

    return updated_city


@router.delete("/{city_id}", response_model=schemas.CityResponse)
def delete_city(
    city_id: int,
    db: Session = Depends(get_db),
):
    city = crud.delete_city(db, city_id)

    if city is None:
        raise HTTPException(
            status_code=404,
            detail="City not found",
        )

    return city
