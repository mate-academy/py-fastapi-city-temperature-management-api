from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from . import crud
from . import schemas
from city.dependencies import get_db

router = APIRouter()


@router.get("/cities/", response_model=list[schemas.City])
def read_cities(db: Session = Depends(get_db)):
    return crud.get_all_cities(db=db)


@router.get("/cities/{city_id}/", response_model=schemas.City)
def read_single_city(city_id: int, db: Session = Depends(get_db)):
    return crud.get_city_by_id(city_id=city_id, db=db)


@router.post("/cities/", response_model=schemas.City)
def create_city(
        city: schemas.CityCreate,
        db: Session = Depends(get_db)
):
    return crud.create_city(db=db, city=city)


@router.delete("/cities/{city_id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_city(city_id: int, db: Session = Depends(get_db)):
    crud.delete_city(db=db, city_id=city_id)


@router.put("/cities/{city_id}/", response_model=schemas.City)
def put_city(
        city: schemas.CityCreate,
        city_id: int,
        db: Session = Depends(get_db)
):
    return crud.put_city(db=db, city=city, city_id=city_id)
