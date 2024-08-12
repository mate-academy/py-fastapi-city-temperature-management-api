from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import RedirectResponse

from city_app import crud, schemas
from dependencies import get_db

router = APIRouter()


@router.get("/cities/", response_model=list[schemas.CityListSchema])
def get_cities(db: Session = Depends(get_db)) -> list[schemas.CityListSchema]:
    return crud.get_all_cities(db=db)


@router.post("/cities/", response_model=schemas.CitySchema)
def create_city(
        city: schemas.CityCreateSchema, db: Session = Depends(get_db)
) -> schemas.CitySchema:
    return crud.create_city(db=db, city=city)


@router.get("/cities/{city_id}", response_model=schemas.CitySchema)
def get_city(
        city_id: int,
        db: Session = Depends(get_db)
) -> schemas.CitySchema:
    return crud.get_specific_city(db=db, city_id=city_id)


@router.delete("/cities/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_city(
        city_id: int,
        db: Session = Depends(get_db)) \
        -> RedirectResponse:
    return crud.delete_city(db=db, city_id=city_id)
