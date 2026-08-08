from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from city_crud_api.api import crud, schemas
from city_crud_api.db.engine import get_db

router = APIRouter(
    prefix="/cities",
    tags=["Cities"],
)


@router.post(
    "/",
    response_model=schemas.CityResponse,
    status_code=201,
)
def create_city(
    city: schemas.CityCreate,
    db: Session = Depends(get_db),
):
    return crud.create_new_city(
        city_data=city,
        db=db,
    )


@router.get(
    "/",
    response_model=list[schemas.CityResponse],
)
def read_cities(db: Session = Depends(get_db)):
    return crud.get_all_cities(db=db)


@router.get(
    "/{city_id}",
    response_model=schemas.CityResponse,
)
def read_city(
    city_id: int,
    db: Session = Depends(get_db),
):
    city = crud.retrieve_specific_city(
        db=db,
        city_id=city_id,
    )

    if city is None:
        raise HTTPException(404, "City not found")

    return city