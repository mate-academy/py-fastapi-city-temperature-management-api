from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependencies import get_db
from . import schemas, crud
from .exceptions import CityAlreadyExistsException, CityNotFoundException

router = APIRouter()


@router.get("/cities/", response_model=list[schemas.City])
def read_cities(db: Session = Depends(get_db)):
    return crud.get_all_cities(db=db)


@router.post("/cities/", response_model=schemas.City)
def create_city(
        city: schemas.CityCreate,
        db: Session = Depends(get_db),
):
    db_city = crud.get_city_by_name(db=db, name=city.name)

    if db_city:
        raise CityAlreadyExistsException()

    return crud.create_city(db=db, city=city)


@router.get("/cities/{city_id}/", response_model=schemas.City)
def read_single_city(city_id: int, db: Session = Depends(get_db)):
    db_city = crud.get_city(db=db, city_id=city_id)

    if db_city is None:
        raise CityNotFoundException()

    return db_city


@router.put("/cities/{city_id}/", response_model=schemas.City)
def update_single_city(
        city_id: int,
        city_data: schemas.CityUpdate,
        db: Session = Depends(get_db)
):
    db_city = crud.update_city(
        db=db, city_id=city_id, city_data=city_data
    )

    if db_city is None:
        raise CityNotFoundException()

    return db_city


@router.delete("/cities/{city_id}/", response_model=bool)
def delete_single_city(city_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_city(db=db, city_id=city_id)

    if not deleted:
        raise CityNotFoundException()

    return {"deleted": deleted}
