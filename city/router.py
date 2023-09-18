from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from city import schemas, crud
from dependencies import get_db

router = APIRouter()


@router.get("/cities/", response_model=list[schemas.City])
def list_cities(db: Session = Depends(get_db)):
    return crud.get_all_cities(db=db)


@router.post("/cities/", response_model=schemas.City)
def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    db_city = crud.get_city_by_name(db=db, name=city.name)
    if db_city:
        raise HTTPException(
            status_code=400, detail="This city is already exist in DB"
        )
    return crud.create_city(db=db, city=city)


@router.get("/cities/{city_id}", response_model=schemas.City)
def retrieve_city_by_id(city_id: int, db: Session = Depends(get_db)):
    db_city = crud.get_city_by_id(db=db, city_id=city_id)
    if db_city:
        return db_city
    raise HTTPException(status_code=404, detail="City not found")


@router.put("/cities/{city_id}", response_model=schemas.City)
def update_city_by_id(
    city_id: int,
    updated_city: schemas.CityUpdate,
    db: Session = Depends(get_db),
):
    db_city = crud.get_city_by_id(db=db, city_id=city_id)
    if db_city:
        return crud.update_city(
            db=db, city_id=city_id, updated_city=updated_city
        )
    raise HTTPException(status_code=404, detail="City not found")


@router.delete("/cities/{city_id}", response_model=dict)
def delete_city_by_id(city_id: int, db: Session = Depends(get_db)):
    return crud.delete_city(db=db, city_id=city_id)
