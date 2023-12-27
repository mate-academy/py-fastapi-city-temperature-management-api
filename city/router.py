from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependencies import get_db
from . import schemas, crud

router = APIRouter()


@router.get("/city/", response_model=list[schemas.City])
def get_all_city(db: Session = Depends(get_db)):
    return crud.get_all_city(db=db)


@router.post("/city/", response_model=schemas.City)
def create_city(
    city: schemas.CityCreate,
    db: Session = Depends(get_db),
):
    db_city = crud.create_city(db=db, city=city)

    return db_city


@router.delete("/city/{city_id}/", response_model=list[schemas.City])
def delete_city(city_id: int, db: Session = Depends(get_db)):
    return crud.delete_city(db=db, city_id=city_id)
