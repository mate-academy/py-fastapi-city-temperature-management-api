from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from dependencies import get_db
from city import schemas, crud


router = APIRouter()


@router.get("/cities/", response_model=list[schemas.City])
def read_cities(db: Session = Depends(get_db)):
    return crud.get_all_cities(db=db)


@router.post("/cities/", response_model=schemas.City)
def create_city(
    city: schemas.CityCreate,
    db: Session = Depends(get_db),
):

    return crud.create_city(db=db, city=city)


@router.get("/cities/{city_id}/", response_model=schemas.City)
def read_single_city(
    city_id: int, db: Session = Depends(get_db)
) -> list[schemas.City]:
    db_city = crud.get_city(db=db, city_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city


@router.put("/cities/{city_id}/", response_model=schemas.City)
def update_city(
    city_id: int,
    city_update: schemas.CityUpdate,
    db: Session = Depends(get_db),
):
    updated_city = crud.update_city(db, city_id, city_update)
    if updated_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return updated_city


@router.delete("/cities/{city_id}/", response_model=schemas.City)
def delete_city(
    city_id: int,
    db: Session = Depends(get_db),
):
    return crud.delete_city(db=db, city_id=city_id)
