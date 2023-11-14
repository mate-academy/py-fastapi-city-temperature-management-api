from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import dependencies
from city import crud, schemas
from dependencies import get_db

router = APIRouter()


@router.get("/cities/", response_model=list[schemas.City])
def cities_list(db: Session = Depends(get_db)):
    return crud.get_cities(db=db)


@router.get("/cities/{city_id}/", response_model=schemas.City)
def retrieve_city(city_id: int, db: Session = Depends(dependencies.get_db)):
    city = crud.get_city_by_id(db, city_id)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@router.post("/cities/", response_model=schemas.CityCreate)
def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    db_city = crud.get_city_by_name(db=db, city_name=city.name)

    if db_city:
        raise HTTPException(
            status_code=400, detail="Such name for city already exists"
        )

    return crud.create_city(db=db, city=city)


@router.put("/cities/{city_id}/", response_model=schemas.City)
def update_city(
    city_id: int, city: schemas.City, db: Session = Depends(get_db)
):
    db_city = crud.get_city_by_id(db=db, city_id=city_id)
    if not db_city:
        raise HTTPException(status_code=400, detail="City not found")
    # TODO: remove this crutch
    city.id = city_id
    return crud.update_city(db=db, city=city)


@router.delete("/cities/{city_id}/")
def delete_city(city_id: int, db: Session = Depends(get_db)):
    db_city = crud.get_city_by_id(db=db, city_id=city_id)

    if not db_city:
        raise HTTPException(status_code=400, detail="City not found")
    return crud.delete_city(db=db, city=db_city)
