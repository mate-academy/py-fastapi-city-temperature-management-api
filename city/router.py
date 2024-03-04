from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException

from . import schemas, crud
from dependencies import get_db

router = APIRouter()


@router.get("/cities", response_model=list[schemas.CityDefault])
def get_all_cities(db: Session = Depends(get_db)):
    return crud.get_all_cities(db)


@router.get("/cities/{city_id}", response_model=schemas.CityDefault)
def get_city_by_id(input_id: int, db: Session = Depends(get_db)):
    db_city = crud.get_city_by_id(db, input_id)
    if not db_city:
        raise HTTPException(
            status_code=400,
            detail=f"City with id={input_id} was not found"
        )
    else:
        return db_city


@router.post("/cities", response_model=schemas.CityDefault,
             status_code=201,
             response_description="Successful Response. City was created")
def create_city(new_city: schemas.CityCreate, db: Session = Depends(get_db)):
    db_city = crud.get_city_by_name(db, new_city.name)
    if db_city:
        raise HTTPException(
            status_code=400,
            detail="City with the same name already exists"
        )
    return crud.create_city(db, new_city)


@router.put("/cities/{city_id}", response_model=schemas.CityDefault,
            response_description="Successful Response. City was updated")
def update_city(input_id: int, updated_city: schemas.CityCreate, db: Session = Depends(get_db)):
    db_city = crud.get_city_by_id(db, input_id)
    if not db_city:
        raise HTTPException(
            status_code=400,
            detail=f"City with id={input_id} was not found"
        )
    return crud.update_city(db, input_id, updated_city)


@router.delete("/cities/{city_id}", response_model=schemas.CityDefault,
               response_description="Successful Response. City was deleted")
def delete_city_by_id(input_id: int, db: Session = Depends(get_db)):
    db_city = crud.get_city_by_id(db, input_id)
    if not db_city:
        raise HTTPException(
            status_code=400,
            detail=f"City with id={input_id} was not found"
        )
    return crud.delete_city_by_id(db, input_id)


