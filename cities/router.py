from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from . import crud, schemas
from dependencies import get_db


router = APIRouter(
    prefix="/cities",
    tags=["Cities"],
)


@router.post("/", response_model=schemas.City, status_code=201)
def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    db_city = crud.get_city_by_name(db=db, name=city.name)

    if db_city:
        raise HTTPException(
            status_code=409,
            detail="City with this name already exists"
        )

    return crud.create_city(db=db, city=city)


@router.get("/", response_model=list[schemas.City])
def read_cities(db: Session = Depends(get_db)):
    return crud.get_all_cities(db=db)


@router.get("/{city_id}", response_model=schemas.City)
def read_single_city(city_id: int, db: Session = Depends(get_db)):
    db_city = crud.get_city(db=db, city_id=city_id)

    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return db_city


@router.put("/{city_id}", response_model=schemas.City)
def update_city(city_id: int, city_data: schemas.CityCreate, db: Session = Depends(get_db)):
    db_city = crud.update_city(db=db, city_id=city_id, city_data=city_data)

    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")

    return db_city


@router.delete("/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_city(city_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_city(db=db, city_id=city_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="City not found")

    return Response(status_code=status.HTTP_204_NO_CONTENT)
