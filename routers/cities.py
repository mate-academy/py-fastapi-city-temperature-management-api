from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from crud import *
import schemas
from crud.city import get_city_by_id
from dependencies import get_db

router = APIRouter()


@router.get("/cities/", tags=["cities"], response_model=list[schemas.CityRead])
def read_cities(db: Annotated[Session, Depends(get_db)]):
    return get_cities(db=db)


@router.get("/cities/{city_id}/", response_model=schemas.CityRead)
def read_single_city(
        city_id: int,
        db: Annotated[Session, Depends(get_db)]
):
    db_city = get_city_by_id(db=db, city_id=city_id)

    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")

    return db_city


@router.post("/cities/", response_model=schemas.CityCreate)
def create_city(
        city: schemas.CityCreate,
        db: Annotated[Session, Depends(get_db)]
):
    db_city = get_city_by_name(db=db, name=city.name)
    if db_city:
        raise HTTPException(
            status_code=400, detail="City with this name already exists"
        )

    return create_one_city(
        db=db,
        city=city
    )


@router.delete(
    "/cities/{city_id}/",
    status_code=status.HTTP_204_NO_CONTENT
)
def remove_city(
        city_id: int,
        db: Session = Depends(get_db),
):
    delete_city(db=db, city_id=city_id)
